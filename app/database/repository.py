from app.config.settings import settings
from app.database.base import SMSCodeRepository, TokenRepository
from app.database.memory_repository import MemorySMSCodeRepository
from app.database.file_repository import FileTokenRepository

# 单例实例
_sms_code_repo: SMSCodeRepository = None
_token_repo: TokenRepository = None

def get_sms_code_repository() -> SMSCodeRepository:
    """获取SMSCode存储实例"""
    global _sms_code_repo
    if _sms_code_repo is None:
        _sms_code_repo = MemorySMSCodeRepository()
    return _sms_code_repo

def get_token_repository() -> TokenRepository:
    """获取Token存储实例"""
    global _token_repo
    if _token_repo is None:
        _token_repo = FileTokenRepository()
    return _token_repo

async def cleanup_expired_data():
    """清理所有过期数据"""
    sms_repo = get_sms_code_repository()
    token_repo = get_token_repository()
    
    sms_count = await sms_repo.cleanup_expired()
    token_count = await token_repo.cleanup_expired()
    
    return {
        "sms_codes_cleaned": sms_count,
        "tokens_cleaned": token_count
    }
