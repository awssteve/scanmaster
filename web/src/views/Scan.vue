<template>
  <div class="scan">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>智能扫描</span>
        </div>
      </template>

      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="上传图片" />
        <el-step title="图像处理" />
        <el-step title="OCR识别" />
        <el-step title="完成" />
      </el-steps>

      <div class="upload-section" v-if="currentStep === 0">
        <el-upload
          class="upload-demo"
          drag
          :auto-upload="false"
          :on-change="handleFileChange"
          :limit="1"
          accept="image/*"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            将图片拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 JPG/PNG/GIF/WEBP 格式，最大 50MB
            </div>
          </template>
        </el-upload>

        <div class="options">
          <el-checkbox v-model="enhance">图像增强</el-checkbox>
          <el-checkbox v-model="autoCrop">自动裁剪</el-checkbox>
        </div>

        <div class="actions">
          <el-button
            type="primary"
            :loading="loading"
            :disabled="!selectedFile"
            @click="handleScan"
          >
            开始扫描
          </el-button>
        </div>
      </div>

      <div class="processing-section" v-if="currentStep === 1">
        <div class="processing-content">
          <el-icon class="is-loading" :size="48" color="#409EFF">
            <Loading />
          </el-icon>
          <p>正在处理图像...</p>
        </div>
      </div>

      <div class="ocr-section" v-if="currentStep === 2">
        <div class="ocr-content">
          <el-icon class="is-loading" :size="48" color="#409EFF">
            <Loading />
          </el-icon>
          <p>正在识别文字...</p>
        </div>
      </div>

      <div class="result-section" v-if="currentStep === 3 && scanResult">
        <div class="result-image">
          <h3>处理后的图像</h3>
          <el-image
            :src="scanResult.image_url"
            fit="contain"
            :preview-src-list="[scanResult.image_url]"
          />
        </div>

        <div class="result-text">
          <h3>识别结果</h3>
          <div class="text-content">
            {{ scanResult.ocr_result.text }}
          </div>
          <div class="text-stats">
            <el-tag type="info">共识别 {{ scanResult.ocr_result.count }} 段</el-tag>
          </div>
        </div>

        <div class="actions">
          <el-button @click="handleCopy">复制文字</el-button>
          <el-button type="primary" @click="handleExportPDF">
            导出PDF
          </el-button>
          <el-button @click="handleReset">重新扫描</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled, Loading } from '@element-plus/icons-vue'
import { scanDocument, type ScanResult } from '@/api'

const router = useRouter()

const currentStep = ref(0)
const selectedFile = ref<File | null>(null)
const enhance = ref(true)
const autoCrop = ref(true)
const loading = ref(false)
const scanResult = ref<ScanResult | null>(null)

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
}

const handleScan = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  loading.value = true
  currentStep.value = 1

  try {
    const result = await scanDocument(
      selectedFile.value,
      enhance.value,
      autoCrop.value
    )
    scanResult.value = result
    currentStep.value = 3
    ElMessage.success('扫描完成')
  } catch (error) {
    currentStep.value = 0
    ElMessage.error('扫描失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleCopy = () => {
  if (!scanResult.value) return

  const text = scanResult.value.ocr_result.text
  navigator.clipboard.writeText(text)
  ElMessage.success('已复制到剪贴板')
}

const handleExportPDF = () => {
  if (!selectedFile.value || !scanResult.value) return

  ElMessage.info('PDF导出功能开发中...')
}

const handleReset = () => {
  currentStep.value = 0
  selectedFile.value = null
  scanResult.value = null
}
</script>

<style scoped>
.scan {
  max-width: 1000px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-section {
  margin-top: 40px;
}

.upload-demo {
  margin-bottom: 30px;
}

.options {
  margin-bottom: 20px;
  text-align: center;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

.processing-section,
.ocr-section {
  padding: 60px 0;
  text-align: center;
}

.processing-content,
.ocr-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.result-section {
  margin-top: 40px;
}

.result-image {
  margin-bottom: 30px;
}

.result-image h3,
.result-text h3 {
  margin: 0 0 20px;
  font-size: 18px;
  color: #333;
}

.result-image .el-image {
  width: 100%;
  max-height: 400px;
  border-radius: 8px;
  overflow: hidden;
}

.text-content {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 14px;
  line-height: 1.8;
  color: #333;
}

.text-stats {
  margin-top: 15px;
}
</style>
