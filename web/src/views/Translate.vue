<template>
  <div class="translate">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>拍照翻译</span>
          <el-button @click="goBack">返回</el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <!-- 左侧：图片上传 -->
        <el-col :xs="24" :md="12">
          <div class="upload-section">
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
                <el-form-item label="源语言：">
                  <el-select v-model="fromLang">
                    <el-option label="中文" value="zh" />
                    <el-option label="英文" value="en" />
                    <el-option label="日文" value="ja" />
                    <el-option label="韩文" value="ko" />
                    <el-option label="法语" value="fr" />
                    <el-option label="德语" value="de" />
                  </el-select>
                </el-form-item>

                <el-form-item label="目标语言：">
                  <el-select v-model="toLang">
                    <el-option label="中文" value="zh" />
                    <el-option label="英文" value="en" />
                    <el-option label="日文" value="ja" />
                    <el-option label="韩文" value="ko" />
                    <el-option label="法语" value="fr" />
                    <el-option label="德语" value="de" />
                  </el-select>
                </el-form-item>
              </el-form>

              <div class="actions">
                <el-button type="primary" :loading="processing" @click="handleTranslate">
                  开始翻译
                </el-button>
              </div>
            </div>

            <div class="image-section" v-if="selectedFile">
              <el-divider />
              <h3>原始图片</h3>
              <el-image
                :src="imageUrl"
                fit="contain"
                :preview-src-list="[imageUrl]"
                style="max-height: 400px; width: 100%;"
              />
            </div>
          </div>
        </el-col>

        <!-- 右侧：翻译结果 -->
        <el-col :xs="24" :md="12">
          <div class="result-section">
            <el-empty v-if="!translatedResult" description="上传图片开始翻译" />

            <div v-else>
              <h3>OCR识别结果</h3>
              <div class="text-content">
                {{ translatedResult.originalText }}
              </div>

              <el-divider />

              <h3>翻译结果</h3>
              <div class="text-content translated">
                {{ translatedResult.translatedText }}
              </div>

              <div class="actions">
                <el-button @click="handleCopyOriginal">复制原文</el-button>
                <el-button type="primary" @click="handleCopyTranslated">
                  复制译文
                </el-button>
                <el-button @click="handleExportWord">导出Word</el-button>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const selectedFile = ref<File | null>(null)
const processing = ref(false)
const fromLang = ref('zh')
const toLang = ref('en')

const imageUrl = computed(() => {
  return selectedFile.value ? URL.createObjectURL(selectedFile.value) : ''
})

const translatedResult = ref<any>(null)

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
  translatedResult.value = null
}

const handleTranslate = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  processing.value = true
  try {
    // TODO: 调用翻译OCR API
    // const result = await translateOCR(selectedFile.value, fromLang.value, toLang.value)

    // 模拟结果
    translatedResult.value = {
      originalText: '模拟OCR识别结果',
      translatedText: `模拟翻译结果 (${fromLang.value} -> ${toLang.value})`
    }

    ElMessage.success('翻译完成')
  } catch (error) {
    ElMessage.error('翻译失败')
  } finally {
    processing.value = false
  }
}

const handleCopyOriginal = () => {
  if (!translatedResult.value) return

  navigator.clipboard.writeText(translatedResult.value.originalText)
  ElMessage.success('已复制到剪贴板')
}

const handleCopyTranslated = () => {
  if (!translatedResult.value) return

  navigator.clipboard.writeText(translatedResult.value.translatedText)
  ElMessage.success('已复制到剪贴板')
}

const handleExportWord = () => {
  ElMessage.info('Word导出功能开发中...')
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.upload-section,
.result-section {
  padding: 20px;
}

.options {
  margin: 20px 0;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

.image-section {
  margin-top: 30px;
}

.image-section h3,
.result-section h3 {
  margin: 0 0 20px;
  font-size: 18px;
  color: #333;
}

.text-content {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  min-height: 150px;
  max-height: 300px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 14px;
  line-height: 1.8;
  color: #333;
}

.translated {
  border-left: 4px solid #409EFF;
  padding-left: 15px;
}
</style>
