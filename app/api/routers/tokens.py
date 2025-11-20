from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.schemas import (
    TokenCreateRequest, TokenCreateResponse, BasicResponse
)
from app.services.token_service import token_service
from app.api.dependencies import verify_token
from app.config.constants import SuccessMessages, ErrorMessages

router = APIRouter()

@router.post("", response_model=TokenCreateResponse)
async def create_token(request: TokenCreateRequest):
    """创建新的Token"""
    try:
        token = await token_service.create_token(request)
        return TokenCreateResponse(
            success=True,
            message=SuccessMessages.TOKEN_CREATED,
            token=token.token,
            name=token.name,
            created_at=token.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("", response_model=List[TokenCreateResponse])
async def list_tokens(token: str = Depends(verify_token)):
    """获取所有Token列表"""
    tokens = await token_service.list_tokens()
    return [
        TokenCreateResponse(
            success=True,
            token=t.token,
            name=t.name,
            created_at=t.created_at
        ) for t in tokens
    ]

@router.delete("/{token_str}", response_model=BasicResponse)
async def delete_token(token_str: str, token: str = Depends(verify_token)):
    """删除Token"""
    if await token_service.delete_token(token_str):
        return BasicResponse(
            success=True,
            message=SuccessMessages.TOKEN_DELETED
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.TOKEN_NOT_FOUND
        )
