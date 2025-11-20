import asyncio
from datetime import datetime
from typing import Optional, List, Dict
from app.database.base import SMSCodeRepository
from app.models.entities import SMSCode

class MemorySMSCodeRepository(SMSCodeRepository):
    """基于内存的SMSCode存储"""
    
    def __init__(self):
        self._storage: Dict[str, SMSCode] = {}
        self._lock = asyncio.Lock()
    
    async def get_by_tag(self, tag: str) -> Optional[SMSCode]:
        """根据tag获取SMSCode"""
        async with self._lock:
            sms_code = self._storage.get(tag)
            if sms_code and sms_code.expires_at > datetime.now():
                return sms_code
            elif sms_code:
                # 自动清理过期数据
                del self._storage[tag]
            return None
    
    async def create(self, sms_code: SMSCode) -> None:
        """创建SMSCode"""
        async with self._lock:
            self._storage[sms_code.tag] = sms_code
    
    async def delete_by_tag(self, tag: str) -> bool:
        """根据tag删除SMSCode"""
        async with self._lock:
            if tag in self._storage:
                del self._storage[tag]
                return True
            return False
    
    async def increment_read_count(self, tag: str) -> bool:
        """增加读取计数"""
        async with self._lock:
            sms_code = self._storage.get(tag)
            if sms_code:
                sms_code.read_count += 1
                return True
            return False
    
    async def cleanup_expired(self) -> int:
        """清理过期数据"""
        async with self._lock:
            current_time = datetime.now()
            expired_tags = [
                tag for tag, sms_code in self._storage.items()
                if sms_code.expires_at <= current_time
            ]
            
            for tag in expired_tags:
                del self._storage[tag]
            
            return len(expired_tags)
    
    async def get_stats(self) -> Dict:
        """获取存储统计信息"""
        async with self._lock:
            current_time = datetime.now()
            active_codes = [
                sms_code for sms_code in self._storage.values()
                if sms_code.expires_at > current_time
            ]
            
            return {
                "total_codes": len(self._storage),
                "active_codes": len(active_codes),
                "expired_codes": len(self._storage) - len(active_codes)
            }
