"""
配置管理模块
包含应用的所有配置设置和常量定义
"""

from .settings import settings, get_redis_url, ensure_directories, add_env_tokens
from .database import database_config
from .security import security_config
from .constants import (
    APIPaths,
    ErrorMessages,
    SuccessMessages,
    LogMessages,
    TimeConstants,
    DefaultValues,
    Environments
)

__all__ = [
    # 主配置
    "settings",
    "get_redis_url",
    "ensure_directories",
    "add_env_tokens",
    
    # 配置类
    "database_config",
    "security_config",
    
    # 常量
    "APIPaths",
    "ErrorMessages", 
    "SuccessMessages",
    "LogMessages",
    "TimeConstants",
    "DefaultValues",
    "Environments"
]

__doc__ = """
配置管理模块

包含：
- settings: 主配置类，从环境变量和.env文件读取配置
- database_config: 数据库相关配置
- security_config: 安全相关配置和工具函数
- constants: 应用常量定义

使用示例：
    from app.config import settings, security_config
    
    # 使用配置
    if security_config.is_token_valid(token):
        # 处理业务逻辑
        pass
"""

# 初始化时确保目录存在
ensure_directories()
