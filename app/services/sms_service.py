from datetime import datetime, timedelta
from typing import Optional
from app.database.repository import get_sms_code_repository
from app.models.entities import SMSCode
from app.models.schemas import SMSCodePushRequest
from app.config.settings import settings
from app.config.constants import DefaultValues

class SMSService:
    """短信验证码服务"""
    
    def __init__(self):
        self.sms_repo = get_sms_code_repository()
    
    async def push_code(self, request: SMSCodePushRequest) -> SMSCode:
        """推送验证码"""
        # 计算过期时间
        ttl = request.ttl or settings.DEFAULT_SMS_CODE_TTL
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        # 创建SMSCode实体
        sms_code = SMSCode(
            tag=request.tag,
            code=request.code,
            created_at=datetime.now(),
            expires_at=expires_at,
            metadata=request.metadata or {}
        )
        
        # 存储到数据库
        await self.sms_repo.create(sms_code)
        return sms_code
    
    async def fetch_code(self, tag: str) -> Optional[SMSCode]:
        """获取验证码"""
        sms_code = await self.sms_repo.get_by_tag(tag)
        
        if not sms_code:
            return None
        
        # 检查是否过期
        if sms_code.expires_at < datetime.now():
            await self.sms_repo.delete_by_tag(tag)
            return None
        
        # 检查读取次数限制
        if sms_code.read_count >= settings.MAX_SMS_CODE_READ_COUNT:
            await self.sms_repo.delete_by_tag(tag)
            return None
        
        # 增加读取计数
        await self.sms_repo.increment_read_count(tag)
        return sms_code
    
    async def delete_code(self, tag: str) -> bool:
        """删除验证码"""
        return await self.sms_repo.delete_by_tag(tag)
    
    async def cleanup_expired_codes(self) -> int:
        """清理过期验证码"""
        return await self.sms_repo.cleanup_expired()

# 服务实例
sms_service = SMSService()
