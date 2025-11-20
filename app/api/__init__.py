"""
API模块初始化文件
"""
from fastapi import APIRouter
from app.api.routers import health, tokens, codes
from app.config import settings
from app.config.constants import APIPaths

# 创建主路由
main_router_prefix = '/'.join([settings.API_PREFIX, APIPaths.BASE]).rstrip('/')
api_router = APIRouter(prefix=main_router_prefix)

# 包含子路由
api_router.include_router(health.router, prefix=APIPaths.HEALTH, tags=["health"])

if settings.ENABLE_ROUTER_TOKENS:
    api_router.include_router(tokens.router, prefix=APIPaths.TOKENS, tags=["tokens"])

api_router.include_router(codes.router, prefix=APIPaths.CODES, tags=["codes"])

# 导出公共接口
__all__ = [
    "api_router",
    "health",
    "tokens", 
    "codes"
]

__doc__ = """
API模块

包含所有API路由的初始化和配置
"""