# 智扫通 - Docker部署指南

## 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- NVIDIA Docker（如果使用GPU）

## 快速启动

### 1. 克隆项目

```bash
git clone https://github.com/your-org/scanmaster.git
cd scanmaster
```

### 2. 启动服务

```bash
docker-compose up -d
```

### 3. 访问应用

- 前端：http://localhost
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

## GPU支持

### 安装NVIDIA Docker

```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### 修改docker-compose.yml

```yaml
services:
  backend:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### 重启服务

```bash
docker-compose down
docker-compose up -d
```

## 常用命令

### 查看日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend
```

### 重启服务
```bash
docker-compose restart
```

### 停止服务
```bash
docker-compose down
```

### 更新服务
```bash
docker-compose pull
docker-compose up -d
```

## 数据持久化

默认使用Docker volumes，数据存储在：

- 上传文件：`./backend/uploads`
- 临时文件：`./backend/temp`
- 静态文件：`./backend/static`

## 环境变量

编辑 `docker-compose.yml` 修改环境变量：

```yaml
services:
  backend:
    environment:
      - ENVIRONMENT=production
      - OCR_USE_GPU=True
      - OCR_LANG_DEFAULT=ch
```

## 性能优化

### 1. 使用GPU

确保OCR_USE_GPU=True

### 2. 限制内存

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 4G
```

### 3. 增加worker数量

修改 `backend/Dockerfile`：

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## 故障排查

### 后端无法启动

查看日志：
```bash
docker-compose logs backend
```

常见问题：
1. GPU不可用：检查NVIDIA Docker安装
2. 依赖安装失败：清理缓存重试
3. 端口冲突：修改docker-compose.yml中的端口

### 前端无法访问

1. 检查后端是否正常运行
2. 检查nginx配置
3. 查看nginx日志：`docker-compose logs frontend`

## 生产部署

### 1. 使用HTTPS

使用nginx反向代理 + Let's Encrypt

### 2. 配置域名

修改nginx.conf：
```nginx
server_name scanmaster.example.com;
```

### 3. 监控

使用Prometheus + Grafana

### 4. 日志

使用ELK或Loki

## 备份

### 备份数据

```bash
# 备份上传文件
tar -czf uploads-$(date +%Y%m%d).tar.gz backend/uploads

# 备份数据库（如果使用）
docker-compose exec backend pg_dump -U postgres scanmaster > dump.sql
```

### 恢复数据

```bash
# 恢复上传文件
tar -xzf uploads-20240208.tar.gz -C backend/

# 恢复数据库
cat dump.sql | docker-compose exec -T backend psql -U postgres scanmaster
```
