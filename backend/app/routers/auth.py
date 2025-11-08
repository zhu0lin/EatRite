"""Authentication endpoints."""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings, get_supabase_admin_client
from app.models import UserCreate, UserLogin, User as UserModel


router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")


# Models (for backward compatibility with FastAPI OAuth2)
class Token(UserModel):
    """Token response model."""
    access_token: str
    token_type: str


class TokenData(UserModel):
    """Token data model."""
    user_id: Optional[str] = None
    email: Optional[str] = None


# Fallback dummy database (for development when Supabase is not configured)
fake_users_db = {
    "test@example.com": {
        "email": "test@example.com",
        "full_name": "Test User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "id": "00000000-0000-0000-0000-000000000000",
        "created_at": datetime.now(timezone.utc),
    }
}


# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def authenticate_with_supabase(email: str, password: str) -> Optional[dict]:
    """Authenticate user with Supabase."""
    try:
        supabase = get_supabase_admin_client()
        if not supabase:
            return None
        
        # Use Supabase Auth to sign in
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            return {
                "id": response.user.id,
                "email": response.user.email,
                "full_name": response.user.user_metadata.get("full_name"),
                "created_at": response.user.created_at,
            }
    except Exception as e:
        print(f"Supabase auth error: {e}")
        return None
    
    return None


async def authenticate_fallback(email: str, password: str) -> Optional[dict]:
    """Fallback authentication using fake database."""
    if email in fake_users_db:
        user_dict = fake_users_db[email]
        if verify_password(password, user_dict["hashed_password"]):
            return user_dict
    return None


async def get_current_user_from_token(token: str) -> dict:
    """Extract and validate user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None:
            raise credentials_exception
            
        return {"user_id": user_id, "email": email}
    except JWTError:
        raise credentials_exception


# Endpoints
@router.post("/auth/register")
async def register(user_data: UserCreate):
    """
    Register a new user.
    
    Creates a new user account in Supabase Auth or fallback storage.
    """
    try:
        supabase = get_supabase_admin_client()
        
        if supabase:
            # Register with Supabase
            response = supabase.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password,
                "options": {
                    "data": {
                        "full_name": user_data.full_name
                    }
                }
            })
            
            if response.user:
                return {
                    "message": "User registered successfully",
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "full_name": user_data.full_name,
                    }
                }
        else:
            # Fallback: Add to fake database
            if user_data.email in fake_users_db:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
            fake_users_db[user_data.email] = {
                "email": user_data.email,
                "full_name": user_data.full_name,
                "hashed_password": get_password_hash(user_data.password),
                "id": f"fallback-{len(fake_users_db)}",
                "created_at": datetime.now(timezone.utc),
            }
            
            return {
                "message": "User registered successfully (fallback mode)",
                "user": {
                    "email": user_data.email,
                    "full_name": user_data.full_name,
                }
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/auth/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login endpoint.
    
    Authenticates user and returns JWT access token.
    Uses Supabase Auth or fallback authentication.
    
    For OAuth2 compatibility, use email as username.
    
    Fallback test credentials:
    - username (email): test@example.com
    - password: secret
    """
    # Try Supabase authentication first
    user = await authenticate_with_supabase(form_data.username, form_data.password)
    
    # Fallback to local authentication
    if not user:
        user = await authenticate_fallback(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": str(user["id"]),
            "email": user["email"],
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/auth/login-json")
async def login_json(credentials: UserLogin):
    """
    Login endpoint with JSON body.
    
    Alternative login endpoint that accepts JSON instead of form data.
    """
    # Try Supabase authentication first
    user = await authenticate_with_supabase(credentials.email, credentials.password)
    
    # Fallback to local authentication
    if not user:
        user = await authenticate_fallback(credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": str(user["id"]),
            "email": user["email"],
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user.get("full_name"),
        }
    }


@router.get("/auth/me")
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Get current user.
    
    Returns the currently authenticated user's information.
    Requires a valid JWT token.
    """
    user_data = await get_current_user_from_token(token)
    
    # Try to get full user info from Supabase
    supabase = get_supabase_admin_client()
    if supabase and user_data.get("user_id"):
        try:
            response = supabase.auth.admin.get_user_by_id(user_data["user_id"])
            if response:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "full_name": response.user.user_metadata.get("full_name"),
                    "created_at": response.user.created_at,
                }
        except Exception as e:
            print(f"Error fetching user from Supabase: {e}")
    
    # Fallback: Return data from token or fake database
    email = user_data.get("email")
    if email and email in fake_users_db:
        user = fake_users_db[email]
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user.get("full_name"),
            "created_at": user.get("created_at"),
        }
    
    return user_data


