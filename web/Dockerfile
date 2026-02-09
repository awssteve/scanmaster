FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
# 增加 npm 安装的稳定性
RUN npm install --registry=https://registry.npmmirror.com

COPY . .
RUN npm run build:only

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
