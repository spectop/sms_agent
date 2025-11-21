from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional, Dict, Any, Union
import os
from pathlib import Path

class Settings(BaseSettings):
    
    # Redis configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # Token settings
    AUTH_TOKENS: List[str] = []
    TOKEN_EXPIRATION_TIME: int = 2592000  # in seconds, -1 means no expiration

    # App settings
    DEFAULT_SMS_CODE_TTL: int = 300  # in seconds
    MAX_SMS_CODE_READ_COUNT: int = 3
    LOG_LEVEL: str = "INFO"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # File storage settings
    TOKENS_FILE_PATH: str = "config/tokens.yaml"
    LOGS_DIRECTORY: str = "logs"
    
    # Security settings
    ALLOWED_ORIGINS: List[str] = []
    API_PREFIX: str = ""
    ENABLE_ROUTER_TOKENS: bool = True
    HIDE_API_DOCS: bool = False
    
    # Cleanup settings
    CLEANUP_INTERVAL: int = 3600  # 清理过期数据的间隔（秒）
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# 创建配置实例
settings = Settings()

def get_redis_url() -> str:
    """获取Redis连接URL"""
    password_part = f":{settings.REDIS_PASSWORD}@" if settings.REDIS_PASSWORD else ""
    return f"redis://{password_part}{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"

def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        Path(settings.LOGS_DIRECTORY),
        Path(settings.TOKENS_FILE_PATH).parent
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

async def add_env_tokens():
    """将环境变量中的Token添加到文件存储中"""
    from app.services.token_service import token_service
    for idx, token in enumerate(settings.AUTH_TOKENS):
        name = f"env_token_{idx+1}"
        await token_service.add_env_token(name, token)