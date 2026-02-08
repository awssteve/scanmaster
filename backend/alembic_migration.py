"""
数据库迁移脚本
"""
from alembic.config import main
from alembic import context
from sqlalchemy import engine_from_config
from logging.config import fileConfig
import sys

# 添加项目路径
sys.path.append('.')

from app.models import Base
from app.core.config import settings

# Alembic Config对象
config = context.config

# 设置SQLAlchemy URL
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# 创建engine
connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=config.get_section(config.config_ini_section).get('sqlalchemy.poolclass')
)

# 创建迁移环境
from alembic import environment
env = environment.Environment(
    config=config,
    script_location=config.get_main_option('script_location'),
)

# 获取connection和metadata
connection = connectable.connect()
context.configure(connection=connection)

# 添加model的MetaData
from alembic import op
target_metadata = Base.metadata

# 运行迁移
def run_migrations_offline():
    """离线运行迁移"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    # 升级到最新版本
    op.upgrade(target='head', bind=connection)
    connection.close()

    print("数据库迁移完成！")

if __name__ == '__main__':
    run_migrations_offline()
