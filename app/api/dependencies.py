from fastapi import Header, HTTPException, status
from typing import Optional
from app.services.token_service import token_service
from app.config.constants import ErrorMessages

async def verify_token(authorization: Optional[str] = Header(None)) -> str:
    """Token验证依赖"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_TOKEN
        )
    
    # 提取Bearer token
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_TOKEN
        )
    
    token = authorization.replace("Bearer ", "")
    
    # 验证token
    if not await token_service.validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.TOKEN_EXPIRED
        )
    
    return token
