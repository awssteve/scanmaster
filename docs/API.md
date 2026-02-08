# API文档

## 基础信息

- Base URL: `http://localhost:8000`
- API版本: v1
- 响应格式: JSON

## 通用响应格式

### 成功响应
```json
{
  "success": true,
  "data": {...}
}
```

### 错误响应
```json
{
  "success": false,
  "message": "错误信息"
}
```

## API端点

### 1. 健康检查

**GET** `/health`

检查API和OCR服务状态

**响应:**
```json
{
  "status": "healthy",
  "ocr_ready": true
}
```

---

### 2. OCR文字识别

**POST** `/api/v1/ocr`

识别图片中的文字

**参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file | File | 是 | 图片文件 |
| lang | string | 否 | 语言类型：ch(中文)/en(英文)/ch_en(中英文)，默认ch |

**响应:**
```json
{
  "success": true,
  "data": {
    "text": "完整识别的文字\n多行文本",
    "texts": ["第一段", "第二段", "..."],
    "positions": [[[x1,y1],[x2,y2],[x3,y3],[x4,y4]], ...],
    "count": 10
  }
}
```

**示例:**
```bash
curl -X POST http://localhost:8000/api/v1/ocr \
  -F "file=@/path/to/image.jpg" \
  -F "lang=ch"
```

---

### 3. 文档扫描

**POST** `/api/v1/scan`

拍照扫描，自动处理图片并OCR识别

**参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file | File | 是 | 图片文件 |
| enhance | boolean | 否 | 是否增强图像，默认true |
| auto_crop | boolean | 否 | 是否自动裁剪，默认true |

**响应:**
```json
{
  "success": true,
  "data": {
    "image_url": "/uploads/xxx_enhanced_cropped.jpg",
    "ocr_result": {
      "text": "识别的文字",
      "texts": [...],
      "positions": [...],
      "count": 5
    }
  }
}
```

**示例:**
```bash
curl -X POST http://localhost:8000/api/v1/scan \
  -F "file=@/path/to/photo.jpg" \
  -F "enhance=true" \
  -F "auto_crop=true"
```

---

### 4. PDF导出

**POST** `/api/v1/pdf/export`

将多张图片导出为PDF

**参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| images | File[] | 是 | 图片文件列表 |
| filename | string | 否 | 输出文件名，默认document.pdf |

**响应:**
```json
{
  "success": true,
  "data": {
    "pdf_url": "/static/pdfs/document.pdf"
  }
}
```

**示例:**
```bash
curl -X POST http://localhost:8000/api/v1/pdf/export \
  -F "images=@/path/to/page1.jpg" \
  -F "images=@/path/to/page2.jpg" \
  -F "filename=mydocument.pdf"
```

---

### 5. 文档处理

**POST** `/api/v1/document/process`

完整文档处理流程（增强/裁剪/OCR）

**参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file | File | 是 | 文档文件（图片/PDF） |
| operations | string | 否 | 处理操作（逗号分隔）：enhance,crop,ocr，默认enhance,crop,ocr |

**响应:**
```json
{
  "success": true,
  "data": {
    "enhanced": true,
    "cropped": true,
    "ocr": {
      "text": "识别的文字",
      "texts": [...],
      "positions": [...],
      "count": 8
    }
  }
}
```

**示例:**
```bash
curl -X POST http://localhost:8000/api/v1/document/process \
  -F "file=@/path/to/document.jpg" \
  -F "operations=enhance,crop,ocr"
```

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |

## 限流

- 无限制（开发环境）
- 生产环境建议配置限流中间件

## 认证

当前版本无需认证

## 文件上传限制

- 最大文件大小：50MB
- 支持格式：jpg, jpeg, png, gif, webp, pdf

## 图像处理参数

### 图像增强
- 对比度增强：1.5倍
- 锐化：1.5倍
- 去噪：中值滤波（3x3）

### 自动裁剪
- Canny边缘检测
- 多边形近似
- 四点透视变换

### 图片调整大小
- 最大尺寸：1920px
- 质量保持：90%

## OCR参数

### 语言支持
- ch: 中文
- en: 英文
- ch_en: 中英文

### 模型
- PaddleOCR
- GPU加速（如果可用）
- 文字方向分类

---

*更新时间：2026-02-08*
