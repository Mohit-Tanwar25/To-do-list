import os
import secrets
import jwt
import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from bson import ObjectId
from db_connection import get_users_collection

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "taskmaster-super-secret-production-key-change-in-env-98213")
ALGORITHM = "HS256"
SESSION_COOKIE_NAME = "taskmaster_session"
SESSION_EXPIRE_DAYS = 30

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "").strip()
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "").strip()
GOOGLE_REDIRECT_URI_OVERRIDE = os.getenv("GOOGLE_REDIRECT_URI", "").strip()

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"


def is_google_auth_configured() -> bool:
    """Returns True if Google Client ID and Secret are configured."""
    return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)


def get_redirect_uri(request: Request) -> str:
    """Computes the OAuth redirect URI based on environment or current request."""
    if GOOGLE_REDIRECT_URI_OVERRIDE:
        return GOOGLE_REDIRECT_URI_OVERRIDE
    
    # Use the base URL of the incoming request
    base_url = str(request.base_url).rstrip("/")
    # Handle reverse proxies if forwarded proto is https
    forwarded_proto = request.headers.get("x-forwarded-proto")
    if forwarded_proto and base_url.startswith("http://"):
        base_url = "https://" + base_url[len("http://"):]
        
    return f"{base_url}/auth/google/callback"


def generate_state_token() -> str:
    """Generates a secure random state string to mitigate CSRF attacks."""
    return secrets.token_urlsafe(32)


import urllib.parse

def get_google_authorization_url(state: str, redirect_uri: str) -> str:
    """Builds the Google OAuth2 consent URL."""
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "select_account"
    }
    query_string = urllib.parse.urlencode(params)
    return f"{GOOGLE_AUTH_ENDPOINT}?{query_string}"


async def exchange_google_code_for_user(code: str, redirect_uri: str) -> Dict[str, Any]:
    """Exchanges authorization code for tokens and retrieves user profile from Google."""
    async with httpx.AsyncClient(timeout=15.0) as client:
        token_response = await client.post(
            GOOGLE_TOKEN_ENDPOINT,
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
            headers={"Accept": "application/json"}
        )
        
        if token_response.status_code != 200:
            error_data = token_response.text
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to exchange code with Google: {error_data}"
            )
            
        token_json = token_response.json()
        access_token = token_json.get("access_token")
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google OAuth response did not contain access_token."
            )
            
        userinfo_response = await client.get(
            GOOGLE_USERINFO_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if userinfo_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch user profile from Google."
            )
            
        return userinfo_response.json()


def upsert_user_record(google_user_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Finds or creates a user record in the MongoDB 'users' collection.
    Standardizes the user profile and updates last_login timestamp.
    """
    users_collection = get_users_collection()
    now = datetime.now(timezone.utc)
    
    google_id = str(google_user_info.get("sub", "")).strip()
    email = str(google_user_info.get("email", "")).strip().lower()
    name = google_user_info.get("name") or email.split("@")[0].capitalize()
    picture = google_user_info.get("picture") or ""
    
    if not google_id or not email:
        raise ValueError("Google profile missing required sub or email field.")
        
    existing_user = users_collection.find_one({
        "$or": [
            {"google_id": google_id},
            {"email": email}
        ]
    })
    
    if existing_user:
        users_collection.update_one(
            {"_id": existing_user["_id"]},
            {
                "$set": {
                    "google_id": google_id,
                    "email": email,
                    "name": name,
                    "picture": picture,
                    "last_login": now,
                    "updated_at": now
                }
            }
        )
        user_id = str(existing_user["_id"])
    else:
        result = users_collection.insert_one({
            "google_id": google_id,
            "email": email,
            "name": name,
            "picture": picture,
            "created_at": now,
            "last_login": now,
            "updated_at": now
        })
        user_id = str(result.inserted_id)
        
    return {
        "id": user_id,
        "google_id": google_id,
        "email": email,
        "name": name,
        "picture": picture
    }


def create_session_token(user_data: Dict[str, Any]) -> str:
    """Creates a signed JWT session token containing user identification claims."""
    expire = datetime.now(timezone.utc) + timedelta(days=SESSION_EXPIRE_DAYS)
    payload = {
        "sub": user_data["id"],
        "google_id": user_data.get("google_id", ""),
        "email": user_data.get("email", ""),
        "name": user_data.get("name", ""),
        "picture": user_data.get("picture", ""),
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_session_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and validates a session JWT token."""
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "id": payload.get("sub"),
            "google_id": payload.get("google_id"),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "picture": payload.get("picture")
        }
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_current_user_optional(request: Request) -> Optional[Dict[str, Any]]:
    """FastAPI helper to retrieve the logged-in user from the session cookie or Authorization header."""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    
    # Also check Bearer Authorization header for API flexibility
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):].strip()
            
    if not token:
        return None
        
    return decode_session_token(token)


def get_current_user_required(request: Request) -> Dict[str, Any]:
    """Dependency that strictly requires an authenticated user; raises 401 otherwise."""
    user = get_current_user_optional(request)
    if not user or not user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in with Google to continue."
        )
    return user
