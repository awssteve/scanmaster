# 智扫通 (ScanMaster) - 快速开始

## 项目结构

```
scanmaster/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── services/    # 业务逻辑
│   │   └── config.py    # 配置
│   ├── main.py          # 入口
│   ├── requirements.txt  # 依赖
│   └── start.sh        # 启动脚本
├── web/                 # 网页版（待开发）
├── miniprogram/         # 微信小程序（待开发）
├── harmony/             # 鸿蒙版（待开发）
└── docs/                # 文档（待开发）
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件（可选）：
```bash
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
OCR_USE_GPU=True
```

### 3. 启动服务

**Linux/Mac:**
```bash
bash start.sh
```

**Windows:**
```bash
start.bat
```

或直接运行：
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问API

- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## API端点

### POST /api/v1/ocr
OCR文字识别

**参数:**
- file: 图片文件
- lang: 语言类型 (ch/en/ch_en)

**返回:**
```json
{
  "success": true,
  "data": {
    "text": "识别的文字",
    "texts": ["段落1", "段落2"],
    "positions": [[...]],
    "count": 2
  }
}
```

### POST /api/v1/scan
文档扫描（拍照扫描）

**参数:**
- file: 图片文件
- enhance: 是否增强图像
- auto_crop: 是否自动裁剪

**返回:**
```json
{
  "success": true,
  "data": {
    "image_url": "/uploads/xxx.jpg",
    "ocr_result": {
      "text": "识别的文字",
      ...
    }
  }
}
```

### POST /api/v1/pdf/export
导出PDF

**参数:**
- images: 图片文件列表
- filename: 输出文件名

**返回:**
```json
{
  "success": true,
  "data": {
    "pdf_url": "/static/pdfs/document.pdf"
  }
}
```

### POST /api/v1/document/process
完整文档处理流程

**参数:**
- file: 文档文件
- operations: 处理操作 (enhance,crop,ocr)

**返回:**
```json
{
  "success": true,
  "data": {
    "enhanced": true,
    "cropped": true,
    "ocr": {...}
  }
}
```

## 技术栈

- **后端**: FastAPI
- **OCR**: PaddleOCR
- **图像处理**: OpenCV + Pillow
- **PDF**: PyPDF2

## 开发计划

- [x] 后端OCR服务
- [x] 图像处理服务
- [x] PDF导出服务
- [ ] 网页版前端
- [ ] 微信小程序
- [ ] 鸿蒙版
- [ ] 公众号引流

## 问题反馈

如有问题，请联系开发者：Green

## License

Copyright © 2026 智扫通
