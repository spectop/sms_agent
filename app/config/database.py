from typing import Dict, Any
from app.config.settings import settings

class DatabaseConfig:
    """数据库配置类"""
    
    @staticmethod
    def get_redis_config() -> Dict[str, Any]:
        """获取Redis配置"""
        return {
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
            "db": settings.REDIS_DB,
            "password": settings.REDIS_PASSWORD,
            "encoding": "utf-8",
            "decode_responses": True
        }
    
    @staticmethod
    def get_file_storage_config() -> Dict[str, Any]:
        """获取文件存储配置"""
        return {
            "tokens_file": settings.TOKENS_FILE_PATH,
        }
    
    @staticmethod
    def get_sqlite_config() -> Dict[str, Any]:
        """获取SQLite配置（未来扩展）"""
        return {
            "database_url": "sqlite:///sms_agent.db",
            "echo": settings.DEBUG
        }

# 配置实例
database_config = DatabaseConfig()
