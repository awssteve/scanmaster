<template>
  <view class="container">
    <!-- 扫描按钮 -->
    <view class="scan-btn" @tap="goToScan">
      <image src="/static/scan.png" class="scan-icon" />
      <text>拍照扫描</text>
    </view>

    <!-- 功能列表 -->
    <view class="feature-list">
      <view class="feature-item" @tap="goToIDCard">
        <image src="/static/id-card.png" class="feature-icon" />
        <text>证件扫描</text>
      </view>

      <view class="feature-item" @tap="goToBatch">
        <image src="/static/batch.png" class="feature-icon" />
        <text>批量处理</text>
      </view>

      <view class="feature-item" @tap="goToDocuments">
        <image src="/static/docs.png" class="feature-icon" />
        <text>我的文档</text>
      </view>

      <view class="feature-item" @tap="goToHistory">
        <image src="/static/history.png" class="feature-icon" />
        <text>历史记录</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const goToScan = () => {
  uni.navigateTo({ url: '/pages/scan/index' })
}

const goToIDCard = () => {
  uni.navigateTo({ url: '/pages/id-card/index' })
}

const goToBatch = () => {
  uni.navigateTo({ url: '/pages/batch/index' })
}

const goToDocuments = () => {
  uni.navigateTo({ url: '/pages/documents/index' })
}

const goToHistory = () => {
  uni.navigateTo({ url: '/pages/history/index' })
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 40rpx 20rpx;
}

.scan-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #409EFF;
  border-radius: 24rpx;
  padding: 80rpx 0;
  margin-bottom: 40rpx;
  box-shadow: 0 8rpx 24rpx rgba(64, 158, 255, 0.3);
}

.scan-icon {
  width: 160rpx;
  height: 160rpx;
  margin-bottom: 20rpx;
}

.scan-btn text {
  font-size: 36rpx;
  color: #fff;
  font-weight: bold;
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.feature-item {
  background: #fff;
  border-radius: 16rpx;
  padding: 40rpx 20rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.feature-icon {
  width: 80rpx;
  height: 80rpx;
  margin-bottom: 16rpx;
}

.feature-item text {
  font-size: 28rpx;
  color: #333;
}
</style>
