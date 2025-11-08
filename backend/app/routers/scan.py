"""Image scanning and food analysis endpoints."""

import uuid
from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status

from app.config import settings
from app.dependencies import get_current_user
from app.models import (
    ScanRequest,
    ScanResponse,
    DetectedItem,
    AnalyzeRequest,
    AnalyzeResponse,
    AllergenWarning,
    NutritionInfo,
)


router = APIRouter()


@router.post("/scan-image", response_model=ScanResponse)
async def scan_image(
    file: UploadFile = File(...),
    current_user: Optional[Annotated[dict, Depends(get_current_user)]] = None
):
    """
    Scan an image for food items and barcodes.
    
    This is a Phase 1 MVP endpoint that returns mock data.
    Phase 2 will implement actual computer vision using OpenCV, Pyzbar, and MediaPipe.
    
    Args:
        file: Image file to scan (jpg, png, etc.)
        current_user: Optional authenticated user for personalized analysis
    
    Returns:
        ScanResponse with detected items (currently mock data)
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload an image file."
        )
    
    # Read file for size validation (optional)
    contents = await file.read()
    file_size_mb = len(contents) / (1024 * 1024)
    
    if file_size_mb > 10:  # 10 MB limit
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Maximum size is 10 MB."
        )
    
    # Generate unique scan ID
    scan_id = str(uuid.uuid4())
    
    # TODO Phase 2: Implement actual computer vision
    # - Use OpenCV for image preprocessing
    # - Use Pyzbar for barcode detection
    # - Use MediaPipe for food classification
    
    # Mock response for MVP
    mock_detected_items = [
        DetectedItem(
            item_type="barcode",
            name="Product Barcode",
            barcode="012345678905",
            confidence=0.95,
            bounding_box={"x": 100, "y": 150, "width": 200, "height": 80}
        ),
        DetectedItem(
            item_type="food",
            name="Apple",
            barcode=None,
            confidence=0.87,
            bounding_box={"x": 50, "y": 50, "width": 150, "height": 150}
        ),
    ]
    
    return ScanResponse(
        scan_id=scan_id,
        detected_items=mock_detected_items,
        processing_time_ms=245.3,
        timestamp=datetime.now(timezone.utc),
        status="success",
        message="Mock scan complete. Phase 2 will implement real computer vision."
    )


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_food(
    request: AnalyzeRequest,
    current_user: Optional[Annotated[dict, Depends(get_current_user)]] = None
):
    """
    Analyze a food product for safety and nutritional information.
    
    This is a Phase 1 MVP endpoint that returns mock data.
    Phase 3 will implement:
    - OpenFoodFacts API integration for ingredient data
    - Allergen and dietary restriction conflict detection
    - Personalized safety analysis based on user preferences
    
    Args:
        request: Analysis request with barcode or product name
        current_user: Optional authenticated user for personalized analysis
    
    Returns:
        AnalyzeResponse with safety assessment and recommendations
    """
    # Validate request
    if not request.barcode and not request.product_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either barcode or product_name must be provided."
        )
    
    # Generate unique analysis ID
    analysis_id = str(uuid.uuid4())
    
    # Determine product name
    product_name = request.product_name or f"Product {request.barcode}"
    
    # TODO Phase 3: Implement actual food data analysis
    # - Query OpenFoodFacts API using barcode
    # - Parse ingredient list
    # - Check against user allergies (from preferences)
    # - Check dietary restrictions (vegan, halal, etc.)
    # - Calculate safety score
    
    # Mock user preferences check (if user is authenticated)
    user_allergies = []
    user_dietary_restrictions = []
    
    if current_user:
        # TODO: Fetch actual user preferences from database
        user_allergies = ["peanuts", "tree nuts"]
        user_dietary_restrictions = ["vegan"]
    
    # Mock allergen warnings
    mock_allergen_warnings = [
        AllergenWarning(
            allergen="peanuts",
            severity="high",
            source="Contains peanut oil in ingredients"
        )
    ] if "peanuts" in user_allergies else []
    
    # Mock dietary conflicts
    mock_dietary_conflicts = [
        "Contains milk (not suitable for vegan diet)"
    ] if "vegan" in user_dietary_restrictions else []
    
    # Calculate mock safety score
    is_safe = len(mock_allergen_warnings) == 0 and len(mock_dietary_conflicts) == 0
    safety_score = 85.0 if is_safe else 35.0
    
    # Mock nutrition info
    mock_nutrition = NutritionInfo(
        calories=250.0,
        protein=8.0,
        carbohydrates=30.0,
        fat=12.0,
        fiber=3.0,
        sugar=15.0,
        sodium=180.0
    )
    
    # Mock ingredients
    mock_ingredients = [
        "wheat flour",
        "sugar",
        "peanut oil",
        "milk",
        "salt",
        "baking powder"
    ]
    
    # Mock recommendations
    mock_recommendations = []
    if not is_safe:
        mock_recommendations.append("⚠️ This product contains allergens that match your profile")
        mock_recommendations.append("Consider alternative products without peanuts")
    else:
        mock_recommendations.append("✓ This product appears safe based on your preferences")
        mock_recommendations.append("Moderate consumption recommended due to sugar content")
    
    return AnalyzeResponse(
        analysis_id=analysis_id,
        product_name=product_name,
        barcode=request.barcode,
        is_safe=is_safe,
        safety_score=safety_score,
        allergen_warnings=mock_allergen_warnings,
        dietary_conflicts=mock_dietary_conflicts,
        nutrition_info=mock_nutrition,
        ingredients=mock_ingredients,
        recommendations=mock_recommendations,
        timestamp=datetime.now(timezone.utc),
        status="success",
        message="Mock analysis complete. Phase 3 will implement OpenFoodFacts API integration."
    )


@router.get("/scan-history")
async def get_scan_history(
    current_user: Annotated[dict, Depends(get_current_user)],
    limit: int = 10,
    offset: int = 0
):
    """
    Get user's scan history.
    
    This is a placeholder endpoint for future implementation.
    Will store and retrieve scan/analysis history from the database.
    
    Args:
        current_user: Authenticated user
        limit: Number of results to return
        offset: Pagination offset
    
    Returns:
        List of previous scans and analyses
    """
    # TODO: Implement in Phase 6
    return {
        "message": "Scan history feature coming in Phase 6",
        "scans": [],
        "total": 0,
        "limit": limit,
        "offset": offset
    }

