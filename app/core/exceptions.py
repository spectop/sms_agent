from fastapi import HTTPException, status
from app.config.constants import ErrorMessages

class SMSCodeException(HTTPException):
    """短信验证码异常基类"""
    
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class TokenExpiredException(SMSCodeException):
    """Token过期异常"""
    
    def __init__(self):
        super().__init__(
            detail=ErrorMessages.TOKEN_EXPIRED,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class CodeNotFoundException(SMSCodeException):
    """验证码不存在异常"""
    
    def __init__(self):
        super().__init__(
            detail=ErrorMessages.CODE_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND
        )

class MaxReadCountExceededException(SMSCodeException):
    """最大读取次数异常"""
    
    def __init__(self):
        super().__init__(
            detail=ErrorMessages.MAX_READ_COUNT_EXCEEDED,
            status_code=status.HTTP_400_BAD_REQUEST
        )
