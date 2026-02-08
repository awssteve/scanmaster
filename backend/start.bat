@echo off
REM 智扫通后端启动脚本 (Windows)

echo ========================================
echo     智扫通 - 后端服务启动
echo ========================================
echo.

REM 检查Python版本
echo 检查Python环境...
python --version

REM 创建必要的目录
echo 创建必要的目录...
if not exist uploads mkdir uploads
if not exist temp mkdir temp
if not exist static mkdir static
if not exist static\pdfs mkdir static\pdfs

REM 检查是否安装了依赖
echo 检查Python依赖...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo 依赖未安装，正在安装...
    pip install -r requirements.txt
)

REM 启动服务
echo 启动后端服务...
echo.
echo API文档: http://localhost:8000/docs
echo 健康检查: http://localhost:8000/health
echo.

REM 根据环境变量选择启动方式
if "%ENVIRONMENT%"=="production" (
    echo 生产模式启动...
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
) else (
    echo 开发模式启动...
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
)

pause
