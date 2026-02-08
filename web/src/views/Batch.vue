<template>
  <div class="batch">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>批量处理</span>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <!-- 批量OCR -->
        <el-tab-pane label="批量OCR" name="ocr">
          <div class="upload-section">
            <el-upload
              class="upload-demo"
              drag
              :auto-upload="false"
              :on-change="handleFileChange"
              :on-remove="handleFileRemove"
              multiple
              accept="image/*"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将多个图片拖到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持批量上传，最多50张
                </div>
              </template>
            </el-upload>

            <div class="options">
              <el-form inline>
                <el-form-item label="语言：">
                  <el-select v-model="ocrLang" placeholder="选择语言">
                    <el-option label="中文" value="ch" />
                    <el-option label="英文" value="en" />
                    <el-option label="中英文" value="ch_en" />
                  </el-select>
                </el-form-item>
              </el-form>
            </div>

            <div class="actions">
              <el-button
                type="primary"
                :loading="processing"
                :disabled="selectedFiles.length === 0"
                @click="handleBatchOCR"
              >
                开始批量OCR
              </el-button>
              <el-button @click="handleClear">清空</el-button>
            </div>
          </div>

          <div class="result-section" v-if="ocrResults.length > 0">
            <el-table :data="ocrResults" max-height="400">
              <el-table-column prop="index" label="序号" width="80" />
              <el-table-column prop="text" label="识别文字" show-overflow-tooltip />
              <el-table-column prop="count" label="字数" width="100" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.success ? 'success' : 'danger'">
                    {{ row.success ? '成功' : '失败' }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>

            <div class="batch-actions">
              <el-button @click="handleCopyAll">复制全部</el-button>
              <el-button type="primary" @click="handleExportPDF">
                导出PDF
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <!-- 批量增强 -->
        <el-tab-pane label="批量增强" name="enhance">
          <div class="upload-section">
            <el-upload
              class="upload-demo"
              drag
              :auto-upload="false"
              :on-change="handleFileChange"
              :on-remove="handleFileRemove"
              multiple
              accept="image/*"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将多个图片拖到此处，或<em>点击上传</em>
              </div>
            </el-upload>

            <div class="actions">
              <el-button
                type="primary"
                :loading="processing"
                :disabled="selectedFiles.length === 0"
                @click="handleBatchEnhance"
              >
                开始批量增强
              </el-button>
              <el-button @click="handleClear">清空</el-button>
            </div>
          </div>

          <div class="result-section" v-if="enhancedImages.length > 0">
            <div class="image-grid">
              <div
                v-for="(img, index) in enhancedImages"
                :key="index"
                class="image-item"
              >
                <el-image
                  :src="img.url"
                  fit="contain"
                  :preview-src-list="enhancedImages.map(i => i.url)"
                />
              </div>
            </div>

            <div class="batch-actions">
              <el-button @click="handleExportPDF">导出PDF</el-button>
              <el-button @click="handleCreateLongImage">
                合成长图
              </el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

const activeTab = ref('ocr')
const selectedFiles = ref<File[]>([])
const processing = ref(false)
const ocrLang = ref('ch')
const ocrResults = ref<any[]>([])
const enhancedImages = ref<any[]>([])

const handleFileChange = (file: any) => {
  if (selectedFiles.value.length >= 50) {
    ElMessage.warning('最多支持50张图片')
    return
  }
  selectedFiles.value.push(file.raw)
}

const handleFileRemove = (file: any) => {
  const index = selectedFiles.value.indexOf(file.raw)
  if (index > -1) {
    selectedFiles.value.splice(index, 1)
  }
}

const handleClear = () => {
  selectedFiles.value = []
  ocrResults.value = []
  enhancedImages.value = []
}

const handleBatchOCR = async () => {
  processing.value = true
  try {
    // TODO: 调用批量OCR API
    // const results = await batchOCR(selectedFiles.value, ocrLang.value)

    // 模拟结果
    ocrResults.value = selectedFiles.value.map((file, index) => ({
      index: index + 1,
      text: `模拟识别结果 ${index + 1}`,
      count: 10,
      success: true
    }))

    ElMessage.success('批量OCR完成')
  } catch (error) {
    ElMessage.error('批量OCR失败')
  } finally {
    processing.value = false
  }
}

const handleBatchEnhance = async () => {
  processing.value = true
  try {
    // TODO: 调用批量增强 API
    // const results = await batchEnhance(selectedFiles.value)

    // 模拟结果
    enhancedImages.value = selectedFiles.value.map((file, index) => ({
      url: URL.createObjectURL(file)
    }))

    ElMessage.success('批量增强完成')
  } catch (error) {
    ElMessage.error('批量增强失败')
  } finally {
    processing.value = false
  }
}

const handleCopyAll = () => {
  const text = ocrResults.value.map(r => r.text).join('\n\n')
  navigator.clipboard.writeText(text)
  ElMessage.success('已复制到剪贴板')
}

const handleExportPDF = () => {
  ElMessage.info('PDF导出功能开发中...')
}

const handleCreateLongImage = () => {
  ElMessage.info('长图片合成功能开发中...')
}
</script>

<style scoped>
.upload-section {
  margin-top: 20px;
}

.options {
  margin: 20px 0;
  text-align: center;
}

.actions {
  margin: 20px 0;
  text-align: center;
}

.result-section {
  margin-top: 30px;
}

.batch-actions {
  margin-top: 20px;
  text-align: center;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.image-item {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.image-item .el-image {
  width: 100%;
  height: 100%;
}
</style>
