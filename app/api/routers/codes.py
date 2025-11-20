from fastapi import APIRouter, HTTPException, status, Depends
from app.models.schemas import (
    SMSCodePushRequest, SMSCodePushResponse, 
    SMSCodeFetchRequest, SMSCodeFetchResponse, BasicResponse
)
from app.services.sms_service import sms_service
from app.api.dependencies import verify_token
from app.config.constants import SuccessMessages, ErrorMessages

router = APIRouter()

@router.post("", response_model=SMSCodePushResponse)
async def push_code(request: SMSCodePushRequest, token: str = Depends(verify_token)):
    """推送验证码"""
    sms_code = await sms_service.push_code(request)
    
    return SMSCodePushResponse(
        success=True,
        message=SuccessMessages.CODE_PUSHED,
        tag=sms_code.tag,
        code=sms_code.code,
        created_at=sms_code.created_at,
        expires_at=sms_code.expires_at,
        read_count=sms_code.read_count
    )

@router.post("/fetch", response_model=SMSCodeFetchResponse)
async def fetch_code(request: SMSCodeFetchRequest, token: str = Depends(verify_token)):
    """获取验证码"""
    sms_code = await sms_service.fetch_code(request.tag)
    
    if not sms_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.CODE_NOT_FOUND
        )
    
    return SMSCodeFetchResponse(
        success=True,
        message=SuccessMessages.CODE_FETCHED,
        tag=sms_code.tag,
        code=sms_code.code,
        created_at=sms_code.created_at,
        expires_at=sms_code.expires_at,
        read_count=sms_code.read_count
    )

@router.delete("/{tag}", response_model=BasicResponse)
async def delete_code(tag: str, token: str = Depends(verify_token)):
    """删除验证码"""
    if await sms_service.delete_code(tag):
        return BasicResponse(
            success=True,
            message=SuccessMessages.CODE_DELETED
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.CODE_NOT_FOUND
        )
