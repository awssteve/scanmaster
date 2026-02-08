"""
后端启动脚本 - 用于测试和开发
"""
import uvicorn
import logging
from app.core.config import settings

# 配置日志
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """启动服务"""
    try:
        logger.info("智扫通API启动中...")

        # 启动服务
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.ENVIRONMENT == "development",
            workers=4 if settings.ENVIRONMENT == "production" else 1,
            log_level=settings.LOG_LEVEL
        )

    except Exception as e:
        logger.error(f"服务启动失败: {e}")
        raise

if __name__ == "__main__":
    main()
