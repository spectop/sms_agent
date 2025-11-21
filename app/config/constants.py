"""应用常量定义"""

# API路径常量
class APIPaths:
    BASE = ""
    HEALTH = "/health"
    TOKENS = "/tokens"
    CODES = "/codes"

# 错误消息常量
class ErrorMessages:
    INVALID_TOKEN = "无效的Token"
    TOKEN_EXPIRED = "Token已过期"
    TOKEN_NOT_FOUND = "Token不存在"
    CODE_NOT_FOUND = "验证码不存在"
    CODE_EXPIRED = "验证码已过期"
    MAX_READ_COUNT_EXCEEDED = "验证码读取次数已达上限"
    PERMISSION_DENIED = "权限不足"

# 成功消息常量
class SuccessMessages:
    CODE_PUSHED = "验证码推送成功"
    CODE_FETCHED = "验证码获取成功"
    CODE_DELETED = "验证码删除成功"
    TOKEN_CREATED = "Token创建成功"
    TOKEN_DELETED = "Token删除成功"

# 日志常量
class LogMessages:
    CODE_PUSH = "推送验证码"
    CODE_FETCH = "获取验证码"
    CODE_DELETE = "删除验证码"
    TOKEN_CREATE = "创建Token"
    TOKEN_DELETE = "删除Token"

# 时间常量（秒）
class TimeConstants:
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800

# 默认值常量
class DefaultValues:
    SMS_CODE_TTL = 300  # 5分钟
    MAX_READ_COUNT = 3
    TOKEN_LENGTH = 32

# 环境常量
class Environments:
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
