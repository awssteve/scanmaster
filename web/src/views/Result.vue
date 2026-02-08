<template>
  <div class="result">
    <el-card v-if="result">
      <template #header>
        <div class="card-header">
          <span>扫描结果</span>
          <el-button @click="goBack">返回</el-button>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="文档名称">
          {{ result.name }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatDate(result.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="识别文字数">
          {{ result.textCount }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(result.status)">
            {{ getStatusText(result.status) }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <div class="result-content">
        <div class="result-image" v-if="result.image_url">
          <h3>处理后的图像</h3>
          <el-image
            :src="result.image_url"
            fit="contain"
            :preview-src-list="[result.image_url]"
          />
        </div>

        <div class="result-text">
          <h3>识别结果</h3>
          <div class="text-content">
            {{ result.text }}
          </div>
          <div class="actions">
            <el-button @click="handleCopy">复制文字</el-button>
            <el-button type="primary" @click="handleExportPDF">
              导出PDF
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <el-skeleton v-else :rows="10" animated />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getDocument } from '@/api'

const route = useRoute()
const router = useRouter()

interface Result {
  id: string
  name: string
  created_at: string
  textCount: number
  status: string
  image_url?: string
  text: string
}

const result = ref<Result | null>(null)

const loadResult = async () => {
  try {
    const id = route.params.id as string
    const data = await getDocument(id)
    result.value = data
  } catch (error) {
    ElMessage.error('加载结果失败')
    goBack()
  }
}

const handleCopy = () => {
  if (!result.value) return

  const text = result.value.text
  navigator.clipboard.writeText(text)
  ElMessage.success('已复制到剪贴板')
}

const handleExportPDF = () => {
  ElMessage.info('PDF导出功能开发中...')
}

const goBack = () => {
  router.back()
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    success: 'success',
    processing: 'warning',
    failed: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    success: '已完成',
    processing: '处理中',
    failed: '失败'
  }
  return map[status] || status
}

onMounted(() => {
  loadResult()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-content {
  margin-top: 30px;
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

.actions {
  margin-top: 20px;
  text-align: center;
}
</style>
