from fastapi import APIRouter, Depends
from schema import image as image_schema
from core.dependencies import get_current_user
from db.models import User
from service import generation as generation_service

router = APIRouter(
    tags=["generation"]
)

@router.post("/generate-image")
async def generate_image(
    request: image_schema.ImageGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a portrait image based on detailed physical description
    """
    return await generation_service.generate_portrait(request)
