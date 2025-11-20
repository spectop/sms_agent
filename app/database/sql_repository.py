"""
SQL存储实现（未来扩展）
"""
from app.database.base import TokenRepository
from app.models.entities import Token

class SQLTokenRepository(TokenRepository):
    """基于SQL的Token存储（未来实现）"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    async def get_by_token(self, token: str):
        # TODO: SQL实现
        pass
    
    async def create(self, token: Token):
        # TODO: SQL实现
        pass
    
    # ... 其他方法占位
