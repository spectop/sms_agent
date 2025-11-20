"""
数据库模块
包含数据存储的抽象和具体实现
"""

from .base import (
    SMSCodeRepository,
    TokenRepository,
)

from .memory_repository import MemorySMSCodeRepository
from .file_repository import FileTokenRepository
from .repository import (
    get_sms_code_repository,
    get_token_repository,
    cleanup_expired_data
)

__all__ = [
    # 抽象基类
    "SMSCodeRepository",
    "TokenRepository", 
    "LogRepository",
    
    # 具体实现
    "MemorySMSCodeRepository",
    "FileTokenRepository",
    
    # 工厂函数
    "get_sms_code_repository",
    "get_token_repository", 
    "cleanup_expired_data"
]

__doc__ = """
数据库存储模块

当前实现：
- SMSCode: 内存存储 (MemorySMSCodeRepository)
- Token: 文件存储 (FileTokenRepository)  

未来扩展：
- SQLite + Redis 实现已预留接口
"""
