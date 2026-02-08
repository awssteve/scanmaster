# 环境要求

## Python环境

- Python >= 3.10
- pip >= 20.0

## 系统要求

### Linux (Ubuntu 20.04+)
```bash
# 安装Python 3.10
sudo apt update
sudo apt install python3.10 python3-pip

# 安装系统依赖
sudo apt install libgomp1
sudo apt install libsm6 libxext6 libxrender-dev libglib2.0-0
```

### macOS (12.0+)
```bash
# 安装Homebrew（如果没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装Python 3.10
brew install python@3.10
```

### Windows (10/11)
```bash
# 下载Python 3.10
# https://www.python.org/downloads/

# 安装时勾选 "Add Python to PATH"
```

## GPU要求（可选）

### NVIDIA GPU（推荐）
- CUDA >= 11.2
- cuDNN >= 8.2

### 验证GPU
```bash
nvidia-smi
```

## 依赖安装

### 安装Python依赖
```bash
cd backend
pip install -r requirements.txt
```

### PaddleOCR额外依赖
```bash
# Linux
sudo apt install libgomp1

# macOS
brew install libomp

# Windows
# PaddleOCR会自动安装
```

## 环境变量

### 创建.env文件
```bash
cd backend
cp .env.example .env
```

### 编辑.env
```bash
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# OCR配置
OCR_USE_GPU=True
OCR_LANG_DEFAULT=ch

# 日志配置
LOG_LEVEL=INFO
```

## 验证安装

### 启动服务
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 健康检查
```bash
curl http://localhost:8000/health
```

### 查看API文档
```
http://localhost:8000/docs
```

## 常见问题

### 1. PaddleOCR安装失败
**问题：** 找不到PaddleOCR
**解决：**
```bash
pip uninstall paddlepaddle paddleocr
pip install paddleocr
```

### 2. GPU不可用
**问题：** OCR使用CPU，速度慢
**解决：**
```bash
# 检查CUDA
nvidia-smi

# 安装GPU版本的PaddlePaddle
pip uninstall paddlepaddle
pip install paddlepaddle-gpu
```

### 3. OpenCV导入错误
**问题：** 找不到cv2
**解决：**
```bash
pip uninstall opencv-python
pip install opencv-python-headless
```

### 4. 图像库导入错误
**问题：** 找不到PIL
**解决：**
```bash
pip install pillow
```

## 性能优化

### 1. 使用GPU
确保OCR_USE_GPU=True

### 2. 调整图像大小
API中调用resize_image(max_size=1920)

### 3. 批量处理
使用ocr_batch接口

### 4. 缓存结果
前端缓存OCR结果，避免重复调用

## 开发工具

### 1. VS Code
推荐扩展：
- Python
- Pylance
- REST Client

### 2. PyCharm
推荐插件：
- Python
- Docker
- REST Client

### 3. Postman
导入API集合进行测试

## 生产环境部署

### Docker部署
```bash
docker build -t scanmaster .
docker run -p 8000:8000 scanmaster
```

### 系统服务
```bash
# 创建systemd服务
sudo nano /etc/systemd/system/scanmaster.service

# 启动服务
sudo systemctl start scanmaster
sudo systemctl enable scanmaster
```

### Nginx反向代理
```nginx
server {
    listen 80;
    server_name scanmaster.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
