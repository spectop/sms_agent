"""
核心模块初始化文件
"""

from .application import app, create_application
from .exceptions import (
    SMSCodeException, 
    TokenExpiredException, 
    CodeNotFoundException, 
    MaxReadCountExceededException
)

__all__ = [
    "app",
    "create_application",
    "SMSCodeException",
    "TokenExpiredException", 
    "CodeNotFoundException",
    "MaxReadCountExceededException"
]

__doc__ = """
核心模块

包含应用的核心功能和异常定义
- app: 应用实例
- create_application: 创建应用实例的函数
- exceptions: 自定义异常类
"""