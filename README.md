# 智扫通 (ScanMaster)

一款基于AI的智能文档扫描工具，支持多平台（网页/微信小程序/鸿蒙），提供拍照扫描、OCR文字识别、PDF导出等功能。

## 核心优势

- ✅ **完全免费** - 基础功能永久免费，无任何隐形收费
- ✅ **本地处理** - 数据本地处理，绝不外传，安全可靠
- ✅ **快速识别** - AI驱动，秒级响应，准确率高达99%
- ✅ **多平台同步** - 网页版/微信小程序/鸿蒙版，数据同步

## 功能特性

### 核心功能
- 📷 拍照扫描 - 支持拍照或上传图片，自动识别文字
- 🔍 OCR识别 - 支持中文/英文/中英文识别
- 📄 PDF导出 - 多张图片一键导出为PDF
- ✨ 图像增强 - 自动增强对比度、锐化、去噪
- ✂️ 自动裁剪 - 检测文档边界，自动裁剪

### 证件扫描
- 🪪 身份证 - 中国大陆身份证
- 🛂 护照 - 中国护照
- 🚗 驾驶证 - 机动车驾驶证
- 📜 毕业证 - 毕业证书
- 🎓 学生证 - 学生证件

### 文档管理
- 📂 我的文档 - 查看所有扫描文档
- 📜 历史记录 - 查看扫描历史
- 🗑️ 文档删除 - 删除不需要的文档

## 快速开始

### 本地开发

**1. 启动后端：**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**2. 启动前端：**
```bash
cd web
npm install
npm run dev
```

**3. 访问应用：**
- 前端：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

### Docker部署

```bash
docker-compose up -d
```

访问：http://localhost

## 技术栈

### 后端
- Python 3.10
- FastAPI
- PaddleOCR
- OpenCV + Pillow
- SQLAlchemy

### 前端
- Vue 3
- TypeScript
- Element Plus
- Vite

### 部署
- Docker + Docker Compose
- Nginx

## 文档

- [快速开始](./QUICKSTART.md)
- [开发计划](./DEVELOPMENT.md)
- [API文档](./docs/API.md)
- [环境配置](./docs/SETUP.md)
- [Docker部署](./docs/DOCKER.md)
- [项目交付说明](./DELIVERY.md)

## 路线图

### MVP（已完成）
- [x] 网页版
- [x] 基础扫描功能
- [x] OCR识别
- [x] PDF导出
- [x] 证件扫描（5种）

### V2（开发中）
- [ ] 微信小程序
- [ ] 更多证件类型
- [ ] 批量处理
- [ ] 用户系统

### V3（规划中）
- [ ] 鸿蒙版
- [ ] 试卷去手写
- [ ] 拍照翻译
- [ ] 转Word/Excel

## 许可证

Copyright © 2026 智扫通

## 联系方式

如有问题或建议，欢迎联系！
