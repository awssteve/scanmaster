<template>
  <div class="id-card">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>证件扫描</span>
          <el-button @click="goBack">返回</el-button>
        </div>
      </template>

      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="选择证件类型" />
        <el-step title="上传图片" />
        <el-step title="识别处理" />
        <el-step title="完成" />
      </el-steps>

      <div class="card-type-section" v-if="currentStep === 0">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="card in cardTypes" :key="card.type">
            <div class="card-type-card" @click="selectCardType(card)">
              <div class="card-icon">
                <el-icon :size="48" :color="card.color">
                  <component :is="card.icon" />
                </el-icon>
              </div>
              <h3>{{ card.name }}</h3>
              <p>{{ card.desc }}</p>
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="upload-section" v-if="currentStep === 1">
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
            将{{ selectedCardType?.name }}拖到此处，或<em>点击上传</em>
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
          <el-button @click="currentStep = 0">上一步</el-button>
          <el-button
            type="primary"
            :loading="loading"
            :disabled="!selectedFile"
            @click="handleScan"
          >
            开始识别
          </el-button>
        </div>
      </div>

      <div class="processing-section" v-if="currentStep === 2">
        <div class="processing-content">
          <el-icon class="is-loading" :size="48" color="#409EFF">
            <Loading />
          </el-icon>
          <p>正在识别{{ selectedCardType?.name }}...</p>
        </div>
      </div>

      <div class="result-section" v-if="currentStep === 3 && scanResult">
        <div class="result-image">
          <h3>证件图片</h3>
          <el-image
            :src="scanResult.image_url"
            fit="contain"
            :preview-src-list="[scanResult.image_url]"
          />
        </div>

        <div class="result-info">
          <h3>识别信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item
              v-for="(value, key) in scanResult.id_info"
              :key="key"
              :label="getLabel(key)"
            >
              {{ value || "未识别" }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="result-ocr">
          <h3>OCR识别结果</h3>
          <div class="text-content">
            {{ scanResult.ocr_result.text }}
          </div>
        </div>

        <div class="actions">
          <el-button @click="handleCopy">复制信息</el-button>
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
import { scanIdCard, type IDCardResult } from '@/api'

const router = useRouter()

const currentStep = ref(0)
const selectedCardType = ref<any>(null)
const selectedFile = ref<File | null>(null)
const enhance = ref(true)
const autoCrop = ref(true)
const loading = ref(false)
const scanResult = ref<IDCardResult | null>(null)

const cardTypes = [
  {
    type: 'id_card',
    name: '身份证',
    desc: '中国大陆身份证',
    icon: 'IdCard',
    color: '#409EFF'
  },
  {
    type: 'passport',
    name: '护照',
    desc: '中国护照',
    icon: 'Document',
    color: '#67C23A'
  },
  {
    type: 'license',
    name: '驾驶证',
    desc: '机动车驾驶证',
    icon: 'Van',
    color: '#E6A23C'
  },
  {
    type: 'graduation',
    name: '毕业证',
    desc: '毕业证书',
    icon: 'Reading',
    color: '#F56C6C'
  },
  {
    type: 'student_card',
    name: '学生证',
    desc: '学生证件',
    icon: 'User',
    color: '#909399'
  }
]

const selectCardType = (card: any) => {
  selectedCardType.value = card
  currentStep.value = 1
}

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
}

const handleScan = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  loading.value = true
  currentStep.value = 2

  try {
    const result = await scanIdCard(
      selectedFile.value,
      selectedCardType.value.type,
      enhance.value,
      autoCrop.value
    )
    scanResult.value = result
    currentStep.value = 3
    ElMessage.success('证件识别完成')
  } catch (error) {
    currentStep.value = 1
    ElMessage.error('证件识别失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleCopy = () => {
  if (!scanResult.value) return

  const info = scanResult.value.id_info
  const text = Object.entries(info)
    .map(([key, value]) => `${getLabel(key)}: ${value || '未识别'}`)
    .join('\n')

  navigator.clipboard.writeText(text)
  ElMessage.success('已复制到剪贴板')
}

const handleExportPDF = () => {
  ElMessage.info('PDF导出功能开发中...')
}

const handleReset = () => {
  currentStep.value = 0
  selectedCardType.value = null
  selectedFile.value = null
  scanResult.value = null
}

const goBack = () => {
  router.back()
}

const getLabel = (key: string) => {
  const labels: Record<string, string> = {
    name: '姓名',
    id_number: '证件号',
    address: '地址',
    phone: '电话',
    issue_date: '发证日期',
    expiry_date: '有效期'
  }
  return labels[key] || key
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-type-section {
  margin-top: 40px;
}

.card-type-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 2px solid transparent;
}

.card-type-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border-color: #409EFF;
}

.card-icon {
  margin-bottom: 20px;
}

.card-type-card h3 {
  margin: 0 0 10px;
  font-size: 18px;
  color: #333;
}

.card-type-card p {
  margin: 0;
  color: #666;
  font-size: 14px;
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

.processing-section {
  padding: 60px 0;
  text-align: center;
}

.processing-content {
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
.result-info h3,
.result-ocr h3 {
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
</style>
