from fastapi import APIRouter, Depends
from app.models.schemas import BasicResponse
from app.api.dependencies import verify_token

router = APIRouter()

@router.get("", response_model=BasicResponse)
async def health_check():
    """健康检查端点"""
    return BasicResponse(
        success=True,
        message="Service is healthy"
    )
