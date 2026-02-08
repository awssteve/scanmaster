# 智扫通 (ScanMaster) - 测试和部署指南

## 测试指南

### 单元测试

**后端测试：**
```bash
cd backend

# 安装测试依赖
pip install pytest pytest-asyncio pytest-cov pytest-mock

# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_ocr_service.py

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html tests/
```

**前端测试：**
```bash
cd web

# 运行单元测试
npm run test

# 运行测试并生成覆盖率报告
npm run test:coverage
```

**E2E测试：**
```bash
cd web

# 运行E2E测试（无头模式）
npm run test:e2e

# 运行E2E测试（有头模式）
npm run test:e2e:headed

# 查看测试报告
npm run test:e2e:report
```

### 性能测试

**OCR性能测试：**
```bash
cd backend

# 运行性能测试
pytest tests/test_performance.py -v -m slow
```

**预期性能：**
- 单张图片OCR：< 5秒
- 批量OCR（10张）：< 1秒
- 图像增强：< 3秒
- PDF导出：< 2秒

---

## 部署指南

### 开发环境部署

**1. 数据库初始化**
```bash
cd backend

# 初始化数据库
python -c "from app.database import init_db; init_db()"

# 运行数据库迁移
python alembic_migration.py
```

**2. 启动后端服务**
```bash
cd backend

# 开发模式
python test_server.py

# 或使用uvicorn
uvicorn main:app --reload
```

**3. 启动前端服务**
```bash
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

**4. 访问应用**
- 前端：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

### 生产环境部署

**1. 使用Docker部署**
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

**2. 手动部署**

**后端：**
```bash
# 安装依赖
pip install -r requirements_v2.txt

# 初始化数据库
python alembic_migration.py

# 启动服务（生产模式）
export ENVIRONMENT=production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level WARNING
```

**前端：**
```bash
# 构建生产版本
npm run build:only

# 使用Nginx部署
# 将dist目录部署到Nginx
```

### 环境变量

**开发环境（.env）：**
```bash
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./scanmaster.db
OCR_USE_GPU=True
OCR_LANG_DEFAULT=ch
LOG_LEVEL=INFO
```

**生产环境（.env.production）：**
```bash
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
DATABASE_URL=postgresql://user:password@localhost:5432/scanmaster
OCR_USE_GPU=True
OCR_LANG_DEFAULT=ch
LOG_LEVEL=WARNING
```

---

## 监控和日志

### 日志配置

**日志级别：**
- 开发环境：INFO
- 生产环境：WARNING

**日志格式：**
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### 监控指标

**关键指标：**
- API响应时间
- OCR识别成功率
- 并发处理能力
- 错误率

**监控工具：**
- Prometheus + Grafana（推荐）
- ELK Stack
- Sentry

---

## 故障排查

### 常见问题

**1. OCR服务初始化失败**
```bash
# 检查PaddleOCR是否正确安装
python -c "from paddleocr import PaddleOCR; ocr = PaddleOCR(); print('OK')"
```

**2. GPU不可用**
```bash
# 检查GPU状态
nvidia-smi

# 如果GPU不可用，设置环境变量
export OCR_USE_GPU=False
```

**3. 数据库连接失败**
```bash
# 检查数据库配置
cat .env

# 检查数据库服务
# PostgreSQL:
psql -h localhost -U postgres
# SQLite:
sqlite3 scanmaster.db
```

**4. 前端无法连接后端**
```bash
# 检查后端服务状态
curl http://localhost:8000/health

# 检查CORS配置
# 确保后端CORS配置正确
```

---

## 性能优化

### 后端优化

**1. 使用异步处理**
```python
# 使用async/await
async def process_image():
    result = await ocr_service.ocr_image(...)
```

**2. 批量处理优化**
```python
# 使用asyncio.gather并发处理
results = await asyncio.gather(*tasks)
```

**3. 数据库优化**
```python
# 使用连接池
engine = create_engine(..., pool_size=10, max_overflow=20)

# 使用批量插入
Session.bulk_save(documents)
```

### 前端优化

**1. 代码分割**
```javascript
// 使用路由懒加载
const route = {
  path: '/documents',
  component: () => import('@/views/Documents.vue')
}
```

**2. 图片懒加载**
```vue
<el-image :src="imageUrl" lazy />
```

**3. 缓存优化**
```javascript
// 使用Pinia状态管理缓存
```

---

## 安全建议

### 后端安全

**1. 认证和授权**
```python
# 使用JWT认证
from app.services.auth_service import get_current_user

@router.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    return {"message": "Hello, " + user.username}
```

**2. 输入验证**
```python
from pydantic import BaseModel, constr

class ImageUpload(BaseModel):
    file: bytes
    lang: constr(regex="^(ch|en|ch_en)$")
```

**3. SQL注入防护**
```python
# 使用SQLAlchemy ORM，自动防护SQL注入
```

### 前端安全

**1. XSS防护**
```vue
<!-- 使用v-html时注意XSS防护 -->
<div v-html="sanitizedHtml"></div>
```

**2. CSRF防护**
```javascript
// 使用axios的CSRF token
axios.defaults.headers.common['X-CSRF-TOKEN'] = getCsrfToken()
```

---

## 备份和恢复

### 数据库备份

**PostgreSQL：**
```bash
# 备份
pg_dump -U postgres scanmaster > backup.sql

# 恢复
psql -U postgres scanmaster < backup.sql
```

**SQLite：**
```bash
# 备份
cp scanmaster.db scanmaster.db.backup

# 恢复
cp scanmaster.db.backup scanmaster.db
```

### 文件备份

**上传文件：**
```bash
# 备份
tar -czf uploads_backup.tar.gz uploads/

# 恢复
tar -xzf uploads_backup.tar.gz
```

---

*更新时间：2026-02-08*
