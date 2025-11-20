"""
数据模型模块
包含应用的所有数据模型定义
"""

from .schemas import (
    BasicResponse,
    SMSCodePushRequest,
    SMSCodePushResponse,
    SMSCodeFetchRequest,
    SMSCodeFetchResponse,
    TokenCreateRequest,
    TokenCreateResponse
)

from .entities import (
    SMSCode,
    Token
)

__all__ = [
    # Schemas
    "BasicResponse",
    "SMSCodePushRequest",
    "SMSCodePushResponse",
    "SMSCodeFetchRequest",
    "SMSCodeFetchResponse",
    "TokenCreateRequest",
    "TokenCreateResponse",

    # Entities
    "SMSCode",
    "Token",
]

# 包级别的文档字符串
__doc__ = """
数据模型模块

包含：
- schemas: Pydantic模型，用于API请求/响应验证
- entities: 业务实体，内部业务逻辑使用  
"""
