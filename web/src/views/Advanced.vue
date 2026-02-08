<template>
  <div class="advanced">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>高级功能</span>
        </div>
      </template>

      <el-row :gutter="20">
        <!-- 去水印 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <div class="feature-card" @click="goToWatermark">
            <div class="card-icon">
              <el-icon :size="48" color="#409EFF">
                <RemoveFilled />
              </el-icon>
            </div>
            <h3>去水印</h3>
            <p>智能去除图片中的水印</p>
          </div>
        </el-col>

        <!-- 翻译 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <div class="feature-card" @click="goToTranslate">
            <div class="card-icon">
              <el-icon :size="48" color="#67C23A">
                <Globe />
              </el-icon>
            </div>
            <h3>拍照翻译</h3>
            <p>OCR识别后自动翻译</p>
          </div>
        </el-col>

        <!-- 转Word -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <div class="feature-card" @click="goToExportWord">
            <div class="card-icon">
              <el-icon :size="48" color="#E6A23C">
                <Document />
              </el-icon>
            </div>
            <h3>转Word</h3>
            <p>导出识别结果为Word文档</p>
          </div>
        </el-col>

        <!-- 转Excel -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <div class="feature-card" @click="goToExportExcel">
            <div class="card-icon">
              <el-icon :size="48" color="#F56C6C">
                <Tickets />
              </el-icon>
            </div>
            <h3>转Excel</h3>
            <p>导出识别结果为Excel表格</p>
          </div>
        </el-col>

        <!-- 长图片 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <div class="feature-card" @click="goToLongImage">
            <div class="card-icon">
              <el-icon :size="48" color="#909399">
                <Link />
              </el-icon>
            </div>
            <h3>长图片</h3>
            <p>多张图片合成为长图</p>
          </div>
        </el-col>

        <!-- 网格图片 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <div class="feature-card" @click="goToGridImage">
            <div class="card-icon">
              <el-icon :size="48" color="#409EFF">
                <Grid />
              </el-icon>
            </div>
            <h3>网格图片</h3>
            <p>多张图片排列为网格</p>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToWatermark = () => {
  router.push('/advanced/watermark')
}

const goToTranslate = () => {
  router.push('/advanced/translate')
}

const goToExportWord = () => {
  router.push('/advanced/export-word')
}

const goToExportExcel = () => {
  router.push('/advanced/export-excel')
}

const goToLongImage = () => {
  router.push('/advanced/long-image')
}

const goToGridImage = () => {
  router.push('/advanced/grid-image')
}
</script>

<style scoped>
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
</style>
