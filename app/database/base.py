from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from app.models.entities import SMSCode, Token

class SMSCodeRepository(ABC):
    """SMSCode存储抽象类"""
    
    @abstractmethod
    async def get_by_tag(self, tag: str) -> Optional[SMSCode]:
        """根据tag获取SMSCode"""
        pass
    
    @abstractmethod
    async def create(self, sms_code: SMSCode) -> None:
        """创建SMSCode"""
        pass
    
    @abstractmethod
    async def delete_by_tag(self, tag: str) -> bool:
        """根据tag删除SMSCode"""
        pass
    
    @abstractmethod
    async def increment_read_count(self, tag: str) -> bool:
        """增加读取计数"""
        pass
    
    @abstractmethod
    async def cleanup_expired(self) -> int:
        """清理过期数据，返回清理数量"""
        pass

class TokenRepository(ABC):
    """Token存储抽象类"""
    
    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[Token]:
        """根据token获取Token信息"""
        pass
    
    @abstractmethod
    async def create(self, token: Token) -> None:
        """创建Token"""
        pass
    
    @abstractmethod
    async def delete_by_token(self, token: str) -> bool:
        """删除Token"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Token]:
        """获取所有Token"""
        pass
    
    @abstractmethod
    async def cleanup_expired(self) -> int:
        """清理过期Token"""
        pass

    @abstractmethod
    async def add_env_token(self, name: str, token: str) -> None:
        """添加环境变量Token"""
        pass
