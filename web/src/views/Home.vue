<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <div class="feature-card" @click="goToScan">
          <div class="card-icon">
            <el-icon :size="48" color="#409EFF">
              <Camera />
            </el-icon>
          </div>
          <h3>拍照扫描</h3>
          <p>拍照或上传图片，自动识别文字</p>
        </div>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <div class="feature-card" @click="goToScan">
          <div class="card-icon">
            <el-icon :size="48" color="#67C23A">
              <Document />
            </el-icon>
          </div>
          <h3>文档识别</h3>
          <p>支持多种文档格式，智能提取文字</p>
        </div>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <div class="feature-card" @click="goToDocuments">
          <div class="card-icon">
            <el-icon :size="48" color="#E6A23C">
              <Files />
            </el-icon>
          </div>
          <h3>PDF导出</h3>
          <p>多张图片一键导出为PDF</p>
        </div>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <div class="feature-card" @click="goToScan">
          <div class="card-icon">
            <el-icon :size="48" color="#F56C6C">
              <IdCard />
            </el-icon>
          </div>
          <h3>证件扫描</h3>
          <p>身份证、护照、驾驶证等证件扫描</p>
        </div>
      </el-col>
    </el-row>

    <el-divider />

    <div class="info-section">
      <h2>为什么选择智扫通？</h2>
      <el-row :gutter="20">
        <el-col :xs="24" :md="8">
          <div class="info-item">
            <div class="info-icon">
              <el-icon :size="32" color="#409EFF">
                <Lightning />
              </el-icon>
            </div>
            <h3>快速识别</h3>
            <p>AI驱动，秒级响应，准确率高达99%</p>
          </div>
        </el-col>

        <el-col :xs="24" :md="8">
          <div class="info-item">
            <div class="info-icon">
              <el-icon :size="32" color="#67C23A">
                <Lock />
              </el-icon>
            </div>
            <h3>隐私保护</h3>
            <p>数据本地处理，绝不外传，安全可靠</p>
          </div>
        </el-col>

        <el-col :xs="24" :md="8">
          <div class="info-item">
            <div class="info-icon">
              <el-icon :size="32" color="#E6A23C">
                <Coin />
              </el-icon>
            </div>
            <h3>完全免费</h3>
            <p>基础功能永久免费，无任何隐形收费</p>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToScan = () => {
  router.push('/scan')
}

const goToDocuments = () => {
  router.push('/documents')
}
</script>

<style scoped>
.home {
  padding: 20px 0;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.card-icon {
  margin-bottom: 20px;
}

.feature-card h3 {
  margin: 0 0 10px;
  font-size: 18px;
  color: #333;
}

.feature-card p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.info-section {
  margin-top: 40px;
}

.info-section h2 {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
}

.info-item {
  text-align: center;
  padding: 20px;
}

.info-icon {
  margin-bottom: 15px;
}

.info-item h3 {
  margin: 0 0 10px;
  font-size: 18px;
  color: #333;
}

.info-item p {
  margin: 0;
  color: #666;
  font-size: 14px;
}
</style>
