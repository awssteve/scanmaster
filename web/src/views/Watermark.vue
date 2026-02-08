<template>
  <div class="watermark">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>水印管理</span>
          <el-button @click="goBack">返回</el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <!-- 去水印 -->
        <el-tab-pane label="去水印" name="remove">
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
          </el-upload>

          <div class="options" v-if="selectedFile">
            <el-form inline label-width="100px">
              <el-form-item label="水印类型：">
                <el-radio-group v-model="watermarkType">
                  <el-radio label="text">文字水印</el-radio>
                  <el-radio label="logo">Logo水印</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="水印文字：" v-if="watermarkType === 'text'">
                <el-input v-model="watermarkText" placeholder="输入水印文字" />
              </el-form-item>
            </el-form>
          </div>

          <div class="actions" v-if="selectedFile">
            <el-button type="primary" :loading="processing" @click="handleRemoveWatermark">
              去水印
            </el-button>
          </div>

          <div class="result-section" v-if="result">
            <el-divider />
            <h3>处理结果</h3>
            <el-image
              :src="result.imageUrl"
              fit="contain"
              :preview-src-list="[result.imageUrl]"
              style="max-height: 400px; width: 100%;"
            />
            <div class="actions">
              <el-button @click="handleDownload">下载</el-button>
            </div>
          </div>
        </el-tab-pane>

        <!-- 添加水印 -->
        <el-tab-pane label="添加水印" name="add">
          <el-upload
            class="upload-demo"
            drag
            :auto-upload="false"
            :on-change="handleFileChangeAdd"
            :limit="1"
            accept="image/*"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将图片拖到此处，或<em>点击上传</em>
            </div>
          </el-upload>

          <div class="options" v-if="selectedFileAdd">
            <el-form inline label-width="100px">
              <el-form-item label="水印文字：">
                <el-input v-model="addWatermarkText" placeholder="输入水印文字" />
              </el-form-item>

              <el-form-item label="位置：">
                <el-select v-model="watermarkPosition">
                  <el-option label="左上" value="top_left" />
                  <el-option label="右上" value="top_right" />
                  <el-option label="左下" value="bottom_left" />
                  <el-option label="右下" value="bottom_right" />
                  <el-option label="居中" value="center" />
                </el-select>
              </el-form-item>

              <el-form-item label="透明度：">
                <el-slider v-model="watermarkOpacity" :min="0" :max="1" :step="0.1" />
              </el-form-item>
            </el-form>
          </div>

          <div class="actions" v-if="selectedFileAdd">
            <el-button type="primary" :loading="processingAdd" @click="handleAddWatermark">
              添加水印
            </el-button>
          </div>

          <div class="result-section" v-if="resultAdd">
            <el-divider />
            <h3>处理结果</h3>
            <el-image
              :src="resultAdd.imageUrl"
              fit="contain"
              :preview-src-list="[resultAdd.imageUrl]"
              style="max-height: 400px; width: 100%;"
            />
            <div class="actions">
              <el-button @click="handleDownloadAdd">下载</el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const activeTab = ref('remove')
const selectedFile = ref<File | null>(null)
const selectedFileAdd = ref<File | null>(null)
const processing = ref(false)
const processingAdd = ref(false)

const watermarkType = ref('text')
const watermarkText = ref('')
const addWatermarkText = ref('智扫通')
const watermarkPosition = ref('bottom_right')
const watermarkOpacity = ref(0.3)

const result = ref<any>(null)
const resultAdd = ref<any>(null)

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
}

const handleFileChangeAdd = (file: any) => {
  selectedFileAdd.value = file.raw
}

const handleRemoveWatermark = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  processing.value = true
  try {
    // TODO: 调用去水印API
    // const data = await removeWatermark(selectedFile.value, watermarkType.value, watermarkText.value)

    // 模拟结果
    result.value = {
      imageUrl: URL.createObjectURL(selectedFile.value)
    }

    ElMessage.success('去水印完成')
  } catch (error) {
    ElMessage.error('去水印失败')
  } finally {
    processing.value = false
  }
}

const handleAddWatermark = async () => {
  if (!selectedFileAdd.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  processingAdd.value = true
  try {
    // TODO: 调用添加水印API
    // const data = await addWatermark(selectedFileAdd.value, addWatermarkText.value, watermarkPosition.value, watermarkOpacity.value)

    // 模拟结果
    resultAdd.value = {
      imageUrl: URL.createObjectURL(selectedFileAdd.value)
    }

    ElMessage.success('水印添加完成')
  } catch (error) {
    ElMessage.error('水印添加失败')
  } finally {
    processingAdd.value = false
  }
}

const handleDownload = () => {
  if (!result.value) return

  const link = document.createElement('a')
  link.href = result.value.imageUrl
  link.download = 'no_watermark.jpg'
  link.click()
}

const handleDownloadAdd = () => {
  if (!resultAdd.value) return

  const link = document.createElement('a')
  link.href = resultAdd.value.imageUrl
  link.download = 'watermarked.jpg'
  link.click()
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.upload-demo {
  margin-top: 20px;
}

.options {
  margin: 20px 0;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

.result-section {
  margin-top: 30px;
}

.result-section h3 {
  margin: 0 0 20px;
  font-size: 18px;
  color: #333;
}
</style>
