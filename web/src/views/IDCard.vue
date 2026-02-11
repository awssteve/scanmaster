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
        <el-step title="拍摄/上传" />
        <el-step title="识别处理" />
        <el-step title="完成" />
      </el-steps>

      <!-- 选择证件类型 -->
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

      <!-- 选择方式 -->
      <div class="method-section" v-if="currentStep === 1 && !selectedMethod">
        <div class="method-cards">
          <div class="method-card" @click="selectMethod('camera')">
            <el-icon :size="48" color="#409EFF"><Camera /></el-icon>
            <h3>拍照扫描</h3>
            <p>使用摄像头直接拍摄</p>
          </div>
          <div class="method-card" @click="selectMethod('upload')">
            <el-icon :size="48" color="#67C23A"><Upload /></el-icon>
            <h3>上传文件</h3>
            <p>从本地上传图片</p>
          </div>
        </div>
      </div>

      <!-- 拍照界面 -->
      <div class="camera-section" v-if="currentStep === 1 && selectedMethod === 'camera'">
        <div class="camera-wrapper">
          <video
            ref="videoRef"
            :class="{ 'mirrored': cameraFacingMode === 'user' }"
            autoplay
            playsinline
            muted
          ></video>
          <canvas ref="canvasRef" style="display: none;"></canvas>

          <div class="camera-controls">
            <el-button
              @click="switchCamera"
              v-if="hasMultipleCameras"
              :icon="Refresh"
              circle
              size="large"
            />
            <el-button
              type="primary"
              @click="capturePhoto"
              :icon="Camera"
              circle
              size="large"
              class="capture-btn"
            />
            <el-button
              @click="closeCamera"
              :icon="Close"
              circle
              size="large"
            />
          </div>

          <div class="camera-message" v-if="cameraError">
            {{ cameraError }}
            <el-button @click="startCamera" style="margin-top: 10px;">重试</el-button>
          </div>
        </div>

        <div class="options" v-if="!cameraError">
          <el-checkbox v-model="enhance">图像增强</el-checkbox>
          <el-checkbox v-model="autoCrop">自动裁剪</el-checkbox>
        </div>

        <div class="preview-section" v-if="capturedImage">
          <h4>预览</h4>
          <img :src="capturedImage" alt="Captured" />
          <div class="preview-actions">
            <el-button @click="retakePhoto">重拍</el-button>
            <el-button type="primary" :loading="loading" @click="handleScan">使用此照片</el-button>
          </div>
        </div>
      </div>

      <!-- 上传界面 -->
      <div class="upload-section" v-if="currentStep === 1 && selectedMethod === 'upload'">
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
          <el-button @click="currentStep = 0; selectedMethod = null">上一步</el-button>
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

      <!-- 处理中 -->
      <div class="processing-section" v-if="currentStep === 2">
        <div class="processing-content">
          <el-icon class="is-loading" :size="48" color="#409EFF">
            <Loading />
          </el-icon>
          <p>正在识别{{ selectedCardType?.name }}...</p>
        </div>
      </div>

      <!-- 结果 -->
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
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled, Loading, Camera, Upload, Refresh, Close } from '@element-plus/icons-vue'
import { scanIdCard, type IDCardResult } from '@/api'

const router = useRouter()

const currentStep = ref(0)
const selectedCardType = ref<any>(null)
const selectedMethod = ref<'camera' | 'upload' | null>(null)
const selectedFile = ref<File | null>(null)
const enhance = ref(true)
const autoCrop = ref(true)
const loading = ref(false)
const scanResult = ref<IDCardResult | null>(null)

// 摄像头相关
const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const cameraFacingMode = ref<'user' | 'environment'>('environment')
const cameraError = ref('')
const capturedImage = ref('')
const hasMultipleCameras = ref(false)
let stream: MediaStream | null = null

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

const selectMethod = (method: 'camera' | 'upload') => {
  selectedMethod.value = method
  if (method === 'camera') {
    startCamera()
  }
}

const startCamera = async () => {
  cameraError.value = ''
  try {
    const devices = await navigator.mediaDevices.enumerateDevices()
    const cameras = devices.filter(d => d.kind === 'videoinput')
    hasMultipleCameras.value = cameras.length > 1

    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: cameraFacingMode.value,
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      },
      audio: false
    })

    if (videoRef.value) {
      videoRef.value.srcObject = stream
    }
  } catch (error: any) {
    console.error('摄像头启动失败:', error)
    if (error.name === 'NotAllowedError') {
      cameraError.value = '请允许访问摄像头'
    } else if (error.name === 'NotFoundError') {
      cameraError.value = '未找到摄像头设备'
    } else {
      cameraError.value = `摄像头启动失败: ${error.message}`
    }
  }
}

const closeCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }
  selectedMethod.value = null
  capturedImage.value = ''
}

const switchCamera = () => {
  cameraFacingMode.value = cameraFacingMode.value === 'user' ? 'environment' : 'user'
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
  startCamera()
}

const capturePhoto = () => {
  if (!videoRef.value || !canvasRef.value) return

  const video = videoRef.value
  const canvas = canvasRef.value
  const context = canvas.getContext('2d')

  if (!context) return

  canvas.width = video.videoWidth
  canvas.height = video.videoHeight

  context.drawImage(video, 0, 0, canvas.width, canvas.height)

  canvas.toBlob((blob) => {
    if (!blob) return

    const file = new File([blob], `camera_${Date.now()}.jpg`, { type: 'image/jpeg' })
    capturedImage.value = URL.createObjectURL(blob)
    selectedFile.value = file
  }, 'image/jpeg', 0.95)
}

const retakePhoto = () => {
  capturedImage.value = ''
  selectedFile.value = null
}

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
}

const handleScan = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先拍照或上传图片')
    return
  }

  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
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
  selectedMethod.value = null
  selectedFile.value = null
  scanResult.value = null
  capturedImage.value = ''
  cameraError.value = ''
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

onUnmounted(() => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.method-cards {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 20px;
}

.method-card {
  flex: 1;
  min-width: 200px;
  max-width: 300px;
  background: white;
  border-radius: 12px;
  padding: 40px 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 2px solid transparent;
}

.method-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border-color: #409EFF;
}

.method-card h3 {
  margin: 20px 0 10px;
  font-size: 18px;
  color: #333;
}

.method-card p {
  margin: 0;
  color: #666;
  font-size: 14px;
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
  margin-bottom: 20px;
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

.camera-section {
  margin-top: 30px;
}

.camera-wrapper {
  position: relative;
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 4/3;
  max-width: 640px;
  margin: 0 auto;
}

.camera-wrapper video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-wrapper video.mirrored {
  transform: scaleX(-1);
}

.camera-controls {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.capture-btn {
  width: 64px;
  height: 64px;
  border: 4px solid white;
}

.camera-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: white;
  padding: 20px;
}

.preview-section {
  margin-top: 20px;
  text-align: center;
}

.preview-section h4 {
  margin: 0 0 15px;
  color: #333;
}

.preview-section img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  border: 2px solid #409EFF;
}

.preview-actions {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.upload-section {
  margin-top: 40px;
}

.upload-demo {
  margin-bottom: 30px;
}

.options {
  margin: 20px 0;
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
