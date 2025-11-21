from typing import List, Set
from app.config.settings import settings
from datetime import datetime, timedelta
import secrets

class SecurityConfig:
    """安全配置类"""
    
    @staticmethod
    def get_allowed_tokens() -> Set[str]:
        """获取允许的token集合"""
        return set(settings.AUTH_TOKENS)
    
    @staticmethod
    def is_token_valid(token: str) -> bool:
        """验证token是否有效"""
        return token in SecurityConfig.get_allowed_tokens()
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """生成新的token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def get_token_expiration() -> timedelta:
        """获取token过期时间"""
        if settings.TOKEN_EXPIRATION_TIME == -1:
            return timedelta(days=365 * 100)  # 100年，相当于永不过期
        return timedelta(seconds=settings.TOKEN_EXPIRATION_TIME)
    
    @staticmethod
    def calculate_expiration_time() -> datetime:
        """计算过期时间"""
        return datetime.now() + SecurityConfig.get_token_expiration()
    
    @staticmethod
    def get_cors_config() -> dict:
        """获取CORS配置"""
        return {
            "allow_origins": settings.ALLOWED_ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }

# 配置实例
security_config = SecurityConfig()
