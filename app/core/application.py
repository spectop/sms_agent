from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.config.settings import settings, ensure_directories, add_env_tokens
from app.config.security import security_config
from app.api import api_router
from app.database.repository import cleanup_expired_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时：确保目录存在
    ensure_directories()
    # 启动时：添加环境变量中的Token
    await add_env_tokens()
    
    # 启动后台清理任务
    cleanup_task = asyncio.create_task(periodic_cleanup())
    
    yield  # 应用运行期间
    
    # 关闭时：取消后台任务
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass

async def periodic_cleanup():
    """定期清理过期数据"""
    while True:
        try:
            await asyncio.sleep(settings.CLEANUP_INTERVAL)
            result = await cleanup_expired_data()
            print(f"清理完成: {result}")
        except Exception as e:
            print(f"清理任务出错: {e}")

def create_application() -> FastAPI:
    """创建FastAPI应用实例"""
    hide_docs = settings.HIDE_API_DOCS
    app = FastAPI(
        title="短信验证码服务",
        description="基于FastAPI的短信验证码推送和获取服务",
        version="1.0.0",
        lifespan=lifespan,
        debug=settings.DEBUG,
        docs_url=None if hide_docs else "/docs",
        redoc_url=None if hide_docs else "/redoc"
    )
    
    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        **security_config.get_cors_config()
    )
    
    # 包含API路由
    app.include_router(api_router)
    
    return app

# 应用实例
app = create_application()

# 运行参数
app_params = {
    "host": settings.HOST,
    "port": settings.PORT
}
