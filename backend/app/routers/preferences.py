"""User preferences endpoints."""

from datetime import datetime, timezone
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import settings, get_supabase_admin_client
from app.dependencies import get_current_user
from app.models import UserPreferences, UserPreferencesCreate, UserPreferencesUpdate


router = APIRouter()


# In-memory fallback storage for preferences when Supabase is not configured
fake_preferences_db = {}


async def get_preferences_from_supabase(user_id: str) -> Optional[dict]:
    """Get user preferences from Supabase."""
    try:
        supabase = get_supabase_admin_client()
        if not supabase:
            return None
        
        response = supabase.table("user_preferences").select("*").eq("user_id", user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception as e:
        print(f"Error fetching preferences from Supabase: {e}")
    
    return None


async def create_preferences_in_supabase(user_id: str, preferences: UserPreferencesCreate) -> Optional[dict]:
    """Create user preferences in Supabase."""
    try:
        supabase = get_supabase_admin_client()
        if not supabase:
            return None
        
        data = {
            "user_id": user_id,
            "allergies": preferences.allergies,
            "dietary_restrictions": preferences.dietary_restrictions,
            "health_goals": preferences.health_goals,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        
        response = supabase.table("user_preferences").insert(data).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception as e:
        print(f"Error creating preferences in Supabase: {e}")
    
    return None


async def update_preferences_in_supabase(user_id: str, preferences: UserPreferencesUpdate) -> Optional[dict]:
    """Update user preferences in Supabase."""
    try:
        supabase = get_supabase_admin_client()
        if not supabase:
            return None
        
        data = {
            "allergies": preferences.allergies,
            "dietary_restrictions": preferences.dietary_restrictions,
            "health_goals": preferences.health_goals,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        
        response = supabase.table("user_preferences").update(data).eq("user_id", user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception as e:
        print(f"Error updating preferences in Supabase: {e}")
    
    return None


@router.get("/preferences", response_model=UserPreferences)
async def get_user_preferences(current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Get user preferences.
    
    Returns the current user's dietary preferences, allergies, and health goals.
    Requires authentication.
    """
    user_id = current_user["user_id"]
    
    # Try Supabase first
    preferences = await get_preferences_from_supabase(user_id)
    
    # Fallback to in-memory storage
    if not preferences:
        preferences = fake_preferences_db.get(user_id)
    
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found. Please create preferences first."
        )
    
    return preferences


@router.post("/preferences", response_model=UserPreferences)
async def create_user_preferences(
    preferences: UserPreferencesCreate,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    """
    Create user preferences.
    
    Creates initial dietary preferences, allergies, and health goals for the user.
    Requires authentication.
    """
    user_id = current_user["user_id"]
    
    # Check if preferences already exist
    existing = await get_preferences_from_supabase(user_id)
    if not existing:
        existing = fake_preferences_db.get(user_id)
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User preferences already exist. Use PUT to update."
        )
    
    # Try to create in Supabase
    result = await create_preferences_in_supabase(user_id, preferences)
    
    # Fallback to in-memory storage
    if not result:
        now = datetime.now(timezone.utc)
        result = {
            "user_id": user_id,
            "allergies": preferences.allergies,
            "dietary_restrictions": preferences.dietary_restrictions,
            "health_goals": preferences.health_goals,
            "created_at": now,
            "updated_at": now,
        }
        fake_preferences_db[user_id] = result
    
    return result


@router.put("/preferences", response_model=UserPreferences)
async def update_user_preferences(
    preferences: UserPreferencesUpdate,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    """
    Update user preferences.
    
    Updates existing dietary preferences, allergies, and health goals.
    Requires authentication.
    """
    user_id = current_user["user_id"]
    
    # Check if preferences exist
    existing = await get_preferences_from_supabase(user_id)
    fallback_mode = False
    
    if not existing:
        existing = fake_preferences_db.get(user_id)
        fallback_mode = True
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found. Use POST to create."
        )
    
    # Try to update in Supabase
    result = await update_preferences_in_supabase(user_id, preferences)
    
    # Fallback to in-memory storage
    if not result or fallback_mode:
        now = datetime.now(timezone.utc)
        result = {
            "user_id": user_id,
            "allergies": preferences.allergies,
            "dietary_restrictions": preferences.dietary_restrictions,
            "health_goals": preferences.health_goals,
            "created_at": existing.get("created_at", now),
            "updated_at": now,
        }
        fake_preferences_db[user_id] = result
    
    return result


@router.delete("/preferences")
async def delete_user_preferences(current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Delete user preferences.
    
    Removes all user preferences.
    Requires authentication.
    """
    user_id = current_user["user_id"]
    
    # Try to delete from Supabase
    try:
        supabase = get_supabase_admin_client()
        if supabase:
            supabase.table("user_preferences").delete().eq("user_id", user_id).execute()
    except Exception as e:
        print(f"Error deleting preferences from Supabase: {e}")
    
    # Also remove from fallback storage
    if user_id in fake_preferences_db:
        del fake_preferences_db[user_id]
    
    return {
        "message": "User preferences deleted successfully"
    }

