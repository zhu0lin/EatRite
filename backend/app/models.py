"""Pydantic models for request/response validation."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID


# User Models
class UserBase(BaseModel):
    """Base user model."""
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation model."""
    password: str


class UserLogin(BaseModel):
    """User login model."""
    email: str
    password: str


class User(UserBase):
    """User response model."""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


# User Preferences Models
class UserPreferencesBase(BaseModel):
    """Base user preferences model."""
    allergies: List[str] = Field(default_factory=list, description="List of food allergies")
    dietary_restrictions: List[str] = Field(
        default_factory=list, 
        description="Dietary restrictions (e.g., vegan, halal, kosher)"
    )
    health_goals: Optional[str] = Field(
        None, 
        description="User's health goals (e.g., weight loss, muscle gain)"
    )


class UserPreferencesCreate(UserPreferencesBase):
    """User preferences creation model."""
    pass


class UserPreferencesUpdate(UserPreferencesBase):
    """User preferences update model."""
    pass


class UserPreferences(UserPreferencesBase):
    """User preferences response model."""
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Scan Models
class ScanRequest(BaseModel):
    """Request model for image scanning."""
    image_filename: str = Field(..., description="Name of the uploaded image file")
    user_id: Optional[UUID] = Field(None, description="User ID for personalized analysis")


class DetectedItem(BaseModel):
    """Model for a detected food item or barcode."""
    item_type: str = Field(..., description="Type: 'food' or 'barcode'")
    name: Optional[str] = Field(None, description="Detected item name")
    barcode: Optional[str] = Field(None, description="Barcode value if detected")
    confidence: float = Field(..., description="Detection confidence score (0-1)")
    bounding_box: Optional[dict] = Field(None, description="Bounding box coordinates")


class ScanResponse(BaseModel):
    """Response model for image scanning."""
    scan_id: str = Field(..., description="Unique scan identifier")
    detected_items: List[DetectedItem] = Field(
        default_factory=list, 
        description="List of detected items"
    )
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="success", description="Scan status")
    message: Optional[str] = Field(None, description="Additional information")


# Analysis Models
class AnalyzeRequest(BaseModel):
    """Request model for food safety analysis."""
    barcode: Optional[str] = Field(None, description="Product barcode")
    product_name: Optional[str] = Field(None, description="Product name")
    user_id: Optional[UUID] = Field(None, description="User ID for personalized analysis")


class AllergenWarning(BaseModel):
    """Model for allergen warnings."""
    allergen: str = Field(..., description="Allergen name")
    severity: str = Field(..., description="Severity: 'high', 'medium', 'low'")
    source: str = Field(..., description="Where allergen was found in ingredients")


class NutritionInfo(BaseModel):
    """Model for nutrition information."""
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    sodium: Optional[float] = None


class AnalyzeResponse(BaseModel):
    """Response model for food safety analysis."""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    product_name: str = Field(..., description="Analyzed product name")
    barcode: Optional[str] = Field(None, description="Product barcode")
    is_safe: bool = Field(..., description="Overall safety assessment")
    safety_score: float = Field(..., description="Safety score (0-100)")
    allergen_warnings: List[AllergenWarning] = Field(
        default_factory=list,
        description="List of allergen warnings"
    )
    dietary_conflicts: List[str] = Field(
        default_factory=list,
        description="Conflicts with user's dietary restrictions"
    )
    nutrition_info: Optional[NutritionInfo] = Field(
        None,
        description="Nutritional information"
    )
    ingredients: List[str] = Field(
        default_factory=list,
        description="List of ingredients"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Personalized recommendations"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="success", description="Analysis status")
    message: Optional[str] = Field(None, description="Additional information")

