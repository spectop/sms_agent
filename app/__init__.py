
"""
短信验证码服务应用包
"""
__version__ = "1.0.0"
__author__ = "SMS Code Service"

# 导出核心应用实例
from .core.application import app, app_params

__all__ = ["app", "app_params"]