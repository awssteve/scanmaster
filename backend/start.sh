#!/bin/bash

# 智扫通后端启动脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    智扫通 - 后端服务启动${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查Python版本
echo -e "${YELLOW}检查Python环境...${NC}"
python3 --version

# 创建必要的目录
echo -e "${YELLOW}创建必要的目录...${NC}"
mkdir -p uploads temp static/pdfs

# 检查是否安装了依赖
echo -e "${YELLOW}检查Python依赖...${NC}"
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo -e "${RED}依赖未安装，正在安装...${NC}"
    pip3 install -r requirements.txt
fi

# 启动服务
echo -e "${GREEN}启动后端服务...${NC}"
echo ""
echo -e "${GREEN}API文档: http://localhost:8000/docs${NC}"
echo -e "${GREEN}健康检查: http://localhost:8000/health${NC}"
echo ""

# 根据环境变量选择启动方式
if [ "$ENVIRONMENT" = "production" ]; then
    echo -e "${YELLOW}生产模式启动...${NC}"
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
else
    echo -e "${YELLOW}开发模式启动...${NC}"
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fi
