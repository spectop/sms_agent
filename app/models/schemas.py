from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class BasicResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class SMSCodePushRequest(BaseModel):
    tag: str
    code: str
    ttl: Optional[int] = None
    metadata: Optional[dict] = None

class SMSCodePushResponse(BasicResponse):
    tag: str
    code: str
    created_at: datetime
    expires_at: datetime
    read_count: int

class SMSCodeFetchRequest(BaseModel):
    tag: str

class SMSCodeFetchResponse(BasicResponse):
    tag: str
    code: str
    created_at: datetime
    expires_at: datetime
    read_count: int

class TokenCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

class TokenCreateResponse(BasicResponse):
    token: str
    name: str
    created_at: datetime
