from datetime import datetime
from typing import List, Optional
from app.database.repository import get_token_repository
from app.models.entities import Token
from app.models.schemas import TokenCreateRequest
from app.config.security import security_config

class TokenService:
    """Token管理服务"""
    
    def __init__(self):
        self.token_repo = get_token_repository()
    
    async def create_token(self, request: TokenCreateRequest) -> Token:
        """创建新的Token"""
        # 生成token
        token_str = security_config.generate_token()
        expires_at = security_config.calculate_expiration_time()
        
        # 创建Token实体
        token = Token(
            token=token_str,
            name=request.name,
            created_at=datetime.now(),
            expires_at=expires_at,
            description=request.description or ""
        )
        
        # 存储到数据库
        await self.token_repo.create(token)
        return token
    
    async def validate_token(self, token: str) -> bool:
        """验证Token是否有效"""
        token_obj = await self.token_repo.get_by_token(token)
        return token_obj is not None
    
    async def get_token_info(self, token: str) -> Optional[Token]:
        """获取Token信息"""
        return await self.token_repo.get_by_token(token)
    
    async def list_tokens(self) -> List[Token]:
        """获取所有Token列表"""
        return await self.token_repo.list_all()
    
    async def delete_token(self, token: str) -> bool:
        """删除Token"""
        return await self.token_repo.delete_by_token(token)
    
    async def cleanup_expired_tokens(self) -> int:
        """清理过期Token"""
        return await self.token_repo.cleanup_expired()
    
    async def add_env_token(self, name: str, token: str) -> None:
        """添加环境变量中的Token"""
        await self.token_repo.add_env_token(name, token)

# 服务实例
token_service = TokenService()
