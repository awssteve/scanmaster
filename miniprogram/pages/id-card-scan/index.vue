<template>
  <view class="container">
    <view class="header">
      <text class="title">{{ cardName }}</text>
      <view class="header-btn" @tap="goBack">返回</view>
    </view>

    <!-- 扫描区域 -->
    <view class="scan-area">
      <image
        :src="imageUrl || '/static/placeholder.png'"
        class="scan-image"
        @tap="chooseImage"
      />
      <text class="tip" v-if="!imageUrl">点击图片开始扫描</text>
    </view>

    <!-- 选项 -->
    <view class="options" v-if="imageUrl">
      <view class="option-item">
        <text class="option-label">图像增强</text>
        <switch :checked="enhance" @change="enhance = $event.value" />
      </view>

      <view class="option-item">
        <text class="option-label">自动裁剪</text>
        <switch :checked="autoCrop" @change="autoCrop = $event.value" />
      </view>
    </view>

    <!-- 扫描按钮 -->
    <view class="scan-btn" @tap="handleScan" v-if="imageUrl">
      <text class="scan-text">{{ scanning ? '扫描中...' : '开始扫描' }}</text>
    </view>

    <!-- 识别结果 -->
    <view class="result-section" v-if="scanResult">
      <view class="result-header">证件信息</view>

      <view class="info-list">
        <view class="info-item" v-for="(value, key) in scanResult.id_info" :key="key">
          <text class="info-label">{{ getLabel(key) }}：</text>
          <text class="info-value">{{ value || '未识别' }}</text>
        </view>
      </view>

      <view class="result-header">OCR识别结果</view>
      <text class="ocr-text">{{ scanResult.ocr_result.text }}</text>

      <view class="result-actions">
        <view class="action-btn" @tap="handleCopy">复制</view>
        <view class="action-btn primary" @tap="handleSave">保存</view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onLoad } from 'vue'

const cardType = ref('')
const cardName = ref('')
const imageUrl = ref('')
const enhance = ref(true)
const autoCrop = ref(true)
const scanning = ref(false)
const scanResult = ref(null)

onLoad((options) => {
  cardType.value = options.type || ''
  cardName.value = options.name || ''
})

const chooseImage = () => {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      imageUrl.value = res.tempFilePaths[0]
      scanResult.value = null
    }
  })
}

const handleScan = () => {
  if (!imageUrl.value) return

  scanning.value = true
  uni.showLoading({ title: '扫描中...' })

  // TODO: 调用后端扫描API
  setTimeout(() => {
    // 模拟结果
    scanResult.value = {
      card_type: cardType.value,
      image_url: imageUrl.value,
      ocr_result: {
        text: '模拟OCR识别结果',
        texts: ['第一段', '第二段'],
        count: 2
      },
      id_info: {
        name: '张三',
        id_number: '身份证号',
        address: '地址信息'
      }
    }

    uni.hideLoading()
    scanning.value = false
    uni.showToast({ title: '扫描完成' })
  }, 2000)
}

const handleCopy = () => {
  if (!scanResult.value) return

  const text = JSON.stringify(scanResult.value.id_info, null, 2)
  uni.setClipboardData({
    data: text
  })

  uni.showToast({ title: '已复制' })
}

const handleSave = () => {
  uni.showToast({ title: '保存成功' })
}

const goBack = () => {
  uni.navigateBack()
}

const getLabel = (key) => {
  const labels = {
    name: '姓名',
    id_number: '证件号',
    address: '地址'
  }
  return labels[key] || key
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

.scan-area {
  margin: 40rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 40rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.scan-image {
  width: 100%;
  height: 800rpx;
  border-radius: 8rpx;
  background: #f5f7fa;
}

.tip {
  position: absolute;
  font-size: 28rpx;
  color: #999;
}

.options {
  margin: 20rpx 40rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
}

.option-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
}

.option-label {
  font-size: 28rpx;
  color: #333;
}

.scan-btn {
  margin: 40rpx;
  background: #409EFF;
  border-radius: 16rpx;
  padding: 40rpx;
  text-align: center;
}

.scan-text {
  font-size: 32rpx;
  color: #fff;
  font-weight: bold;
}

.result-section {
  margin: 20rpx 40rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 40rpx;
}

.result-header {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.info-list {
  margin-bottom: 40rpx;
}

.info-item {
  display: flex;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eee;
}

.info-label {
  font-size: 28rpx;
  color: #666;
  width: 150rpx;
}

.info-value {
  font-size: 28rpx;
  color: #333;
  flex: 1;
}

.ocr-text {
  background: #f5f7fa;
  padding: 30rpx;
  border-radius: 8rpx;
  font-size: 28rpx;
  line-height: 1.8;
  color: #333;
  min-height: 200rpx;
  display: block;
  margin-bottom: 40rpx;
}

.result-actions {
  display: flex;
  gap: 20rpx;
}

.action-btn {
  flex: 1;
  padding: 30rpx;
  border-radius: 8rpx;
  text-align: center;
  font-size: 28rpx;
  color: #666;
  background: #f5f7fa;
}

.action-btn.primary {
  background: #409EFF;
  color: #fff;
}
</style>
