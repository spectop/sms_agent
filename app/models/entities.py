from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class SMSCode:
    tag: str
    code: str
    created_at: datetime
    expires_at: datetime
    read_count: int = 0
    metadata: dict = None

@dataclass
class Token:
    token: str
    name: str
    created_at: datetime
    expires_at: datetime
    description: str = ""
    