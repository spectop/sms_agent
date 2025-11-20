import json
import yaml
import os
from datetime import datetime
from typing import Optional, List, Dict
from app.database.base import TokenRepository
from app.models.entities import Token

class FileTokenRepository(TokenRepository):
    """基于文件的Token存储"""
    
    def __init__(self, tokens_file: str = "config/tokens.yaml"):
        self.tokens_file = tokens_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """确保文件存在"""
        os.makedirs(os.path.dirname(self.tokens_file), exist_ok=True)
        if not os.path.exists(self.tokens_file):
            with open(self.tokens_file, 'w') as f:
                yaml.dump({"tokens": []}, f)
    
    def _load_tokens(self) -> List[Dict]:
        """从文件加载tokens"""
        try:
            with open(self.tokens_file, 'r') as f:
                data = yaml.safe_load(f) or {}
                return data.get("tokens", [])
        except (yaml.YAMLError, FileNotFoundError):
            return []
    
    def _save_tokens(self, tokens_data: List[Dict]):
        """保存tokens到文件"""
        with open(self.tokens_file, 'w') as f:
            yaml.dump({"tokens": tokens_data}, f, default_flow_style=False)
    
    async def get_by_token(self, token: str) -> Optional[Token]:
        """根据token获取Token信息"""
        tokens_data = self._load_tokens()
        
        for token_data in tokens_data:
            if token_data.get("token") == token:
                # 检查是否过期
                expires_at = datetime.fromisoformat(token_data["expires_at"])
                if expires_at > datetime.now():
                    return Token(
                        token=token_data["token"],
                        name=token_data["name"],
                        created_at=datetime.fromisoformat(token_data["created_at"]),
                        expires_at=expires_at,
                        description=token_data.get("description", "")
                    )
                else:
                    # Token过期，自动删除
                    await self.delete_by_token(token)
        
        return None
    
    async def create(self, token: Token) -> None:
        """创建Token"""
        tokens_data = self._load_tokens()
        
        # 检查是否已存在
        for existing_token in tokens_data:
            if existing_token.get("token") == token.token:
                raise ValueError(f"Token {token.token} already exists")
        
        # 添加新token
        tokens_data.append({
            "token": token.token,
            "name": token.name,
            "created_at": token.created_at.isoformat(),
            "expires_at": token.expires_at.isoformat(),
            "description": token.description
        })
        
        self._save_tokens(tokens_data)
    
    async def delete_by_token(self, token: str) -> bool:
        """删除Token"""
        tokens_data = self._load_tokens()
        original_count = len(tokens_data)
        
        tokens_data = [t for t in tokens_data if t.get("token") != token]
        
        if len(tokens_data) < original_count:
            self._save_tokens(tokens_data)
            return True
        return False
    
    async def list_all(self) -> List[Token]:
        """获取所有Token"""
        tokens_data = self._load_tokens()
        current_time = datetime.now()
        
        tokens = []
        expired_tokens = []
        
        for token_data in tokens_data:
            expires_at = datetime.fromisoformat(token_data["expires_at"])
            if expires_at > current_time:
                tokens.append(Token(
                    token=token_data["token"],
                    name=token_data["name"],
                    created_at=datetime.fromisoformat(token_data["created_at"]),
                    expires_at=expires_at,
                    description=token_data.get("description", "")
                ))
            else:
                expired_tokens.append(token_data["token"])
        
        # 异步清理过期token
        if expired_tokens:
            for token in expired_tokens:
                await self.delete_by_token(token)
        
        return tokens
    
    async def cleanup_expired(self) -> int:
        """清理过期Token"""
        tokens_data = self._load_tokens()
        current_time = datetime.now()
        
        original_count = len(tokens_data)
        tokens_data = [
            t for t in tokens_data 
            if datetime.fromisoformat(t["expires_at"]) > current_time
        ]
        
        expired_count = original_count - len(tokens_data)
        if expired_count > 0:
            self._save_tokens(tokens_data)
        
        return expired_count
    
    async def add_env_token(self, name: str, token: str) -> None:
        """添加环境变量Token"""
        tokens_data = self._load_tokens()
        
        # 检查是否已存在
        for existing_token in tokens_data:
            if existing_token.get("token") == token:
                return  # 已存在则不添加

        # 添加新token，环境变量Token不过期
        tokens_data.append({
            "token": token,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.max).isoformat(),
            "description": "Environment Variable Token"
        })
        
        self._save_tokens(tokens_data)
