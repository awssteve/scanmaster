<template>
  <view class="container">
    <view class="header">
      <text class="title">批量处理</text>
      <view class="header-btn" @tap="goBack">返回</view>
    </view>

    <!-- 文件选择 -->
    <view class="upload-section">
      <view class="section-title">选择文件（{{ files.length }}/50）</view>
      <view class="file-list" v-if="files.length > 0">
        <view
          class="file-item"
          v-for="(file, index) in files"
          :key="index"
        >
          <image :src="file.url" class="file-thumb" />
          <view class="file-info">
            <text class="file-name">{{ file.name }}</text>
            <text class="file-size">{{ formatSize(file.size) }}</text>
          </view>
          <view class="file-remove" @tap="removeFile(index)">×</view>
        </view>
      </view>

      <view class="upload-btn" @tap="chooseFiles">
        <image src="/static/add.png" class="add-icon" />
        <text class="add-text">添加文件</text>
      </view>
    </view>

    <!-- 操作类型 -->
    <view class="action-section" v-if="files.length > 0">
      <view class="section-title">选择操作</view>
      <view class="action-grid">
        <view
          class="action-item"
          :class="{ active: activeAction === 'ocr' }"
          @tap="activeAction = 'ocr'"
        >
          <text class="action-name">批量OCR</text>
          <text class="action-desc">文字识别</text>
        </view>

        <view
          class="action-item"
          :class="{ active: activeAction === 'enhance' }"
          @tap="activeAction = 'enhance'"
        >
          <text class="action-name">批量增强</text>
          <text class="action-desc">图像优化</text>
        </view>

        <view
          class="action-item"
          :class="{ active: activeAction === 'export' }"
          @tap="activeAction = 'export'"
        >
          <text class="action-name">导出PDF</text>
          <text class="action-desc">合并文档</text>
        </view>
      </view>
    </view>

    <!-- 开始处理按钮 -->
    <view class="start-btn" v-if="files.length > 0" @tap="handleProcess">
      <text class="start-text">{{ processing ? '处理中...' : '开始处理' }}</text>
    </view>

    <!-- 处理结果 -->
    <view class="result-section" v-if="results.length > 0">
      <view class="section-title">处理结果</view>
      <view class="result-list">
        <view
          class="result-item"
          v-for="(result, index) in results"
          :key="index"
          :class="{ success: result.success, failed: !result.success }"
        >
          <text class="result-status">{{ result.success ? '✓' : '✗' }}</text>
          <text class="result-text">{{ result.message }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const files = ref([])
const activeAction = ref('')
const processing = ref(false)
const results = ref([])

const chooseFiles = () => {
  if (files.value.length >= 50) {
    uni.showToast({ title: '最多50个文件' })
    return
  }

  uni.chooseMessageFile({
    count: 50 - files.value.length,
    type: 'image',
    success: (res) => {
      const newFiles = res.tempFiles.map(f => ({
        name: f.name,
        size: f.size,
        url: f.path
      }))
      files.value = [...files.value, ...newFiles]
    }
  })
}

const removeFile = (index) => {
  files.value.splice(index, 1)
}

const handleProcess = () => {
  if (!activeAction.value) {
    uni.showToast({ title: '请选择操作类型' })
    return
  }

  processing.value = true
  uni.showLoading({ title: '处理中...' })

  // TODO: 调用后端批量处理API
  setTimeout(() => {
    // 模拟结果
    results.value = files.value.map((file, index) => ({
      success: index % 3 !== 0, // 模拟部分失败
      message: `${file.name} ${activeAction.value}处理${index % 3 !== 0 ? '成功' : '失败'}`
    }))

    uni.hideLoading()
    processing.value = false
  }, 3000)
}

const goBack = () => {
  uni.navigateBack()
}

const formatSize = (size) => {
  if (size < 1024) return `${size}B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(2)}KB`
  return `${(size / 1024 / 1024).toFixed(2)}MB`
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f7fa;
}

.header {
  background: #409EFF;
  padding: 30rpx 40rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.title {
  font-size: 36rpx;
  color: #fff;
  font-weight: bold;
}

.header-btn {
  font-size: 28rpx;
  color: #fff;
}

.upload-section,
.action-section,
.result-section {
  margin: 20rpx 40rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.file-list {
  margin-bottom: 20rpx;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eee;
}

.file-thumb {
  width: 80rpx;
  height: 80rpx;
  border-radius: 8rpx;
  background: #f5f7fa;
  margin-right: 20rpx;
}

.file-info {
  flex: 1;
}

.file-name {
  font-size: 28rpx;
  color: #333;
  display: block;
  margin-bottom: 6rpx;
}

.file-size {
  font-size: 24rpx;
  color: #999;
  display: block;
}

.file-remove {
  font-size: 48rpx;
  color: #F56C6C;
  width: 40rpx;
  text-align: center;
}

.upload-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
}

.add-icon {
  width: 80rpx;
  height: 80rpx;
  margin-bottom: 10rpx;
}

.add-text {
  font-size: 28rpx;
  color: #666;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20rpx;
}

.action-item {
  background: #f5f7fa;
  border-radius: 12rpx;
  padding: 30rpx 20rpx;
  text-align: center;
  border: 2rpx solid transparent;
}

.action-item.active {
  border-color: #409EFF;
  background: #ecf5ff;
}

.action-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10rpx;
}

.action-desc {
  font-size: 24rpx;
  color: #999;
  display: block;
}

.start-btn {
  margin: 40rpx;
  background: #409EFF;
  border-radius: 16rpx;
  padding: 40rpx;
  text-align: center;
}

.start-text {
  font-size: 32rpx;
  color: #fff;
  font-weight: bold;
}

.result-list {
  margin-top: 20rpx;
}

.result-item {
  display: flex;
  align-items: center;
  padding: 20rpx;
  border-radius: 8rpx;
  margin-bottom: 10rpx;
  background: #f5f7fa;
}

.result-item.success {
  background: #f0f9ff;
}

.result-item.failed {
  background: #fef0f0;
}

.result-status {
  font-size: 36rpx;
  margin-right: 20rpx;
}

.result-item.success .result-status {
  color: #67C23A;
}

.result-item.failed .result-status {
  color: #F56C6C;
}

.result-text {
  font-size: 28rpx;
  color: #333;
  flex: 1;
}
</style>
