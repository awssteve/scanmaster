<template>
  <view class="container">
    <view class="header">
      <text class="title">历史记录</text>
    </view>

    <view class="history-list" v-if="history.length > 0">
      <view
        class="history-item"
        v-for="(item, index) in history"
        :key="index"
        @tap="viewHistory(item)"
      >
        <view class="history-info">
          <text class="history-name">{{ item.name }}</text>
          <text class="history-time">{{ formatTime(item.timestamp) }}</text>
          <text class="history-count">识别文字数：{{ item.textCount }}</text>
        </view>
        <text class="arrow">></text>
      </view>
    </view>

    <view class="empty" v-else>
      <image src="/static/empty.png" class="empty-icon" />
      <text class="empty-text">暂无历史记录</text>
      <view class="empty-btn" @tap="goToScan">开始扫描</view>
      <view class="clear-btn" @tap="clearHistory">清空历史</view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const history = ref([])

onMounted(() => {
  loadHistory()
})

const loadHistory = () => {
  // TODO: 从后端加载历史记录
  // 模拟数据
  history.value = [
    {
      id: '1',
      name: '证件扫描',
      timestamp: new Date().toISOString(),
      textCount: 10
    },
    {
      id: '2',
      name: '文档扫描',
      timestamp: new Date(Date.now() - 86400000).toISOString(),
      textCount: 20
    }
  ]
}

const viewHistory = (item) => {
  uni.navigateTo({
    url: `/pages/history-result/index?id=${item.id}`
  })
}

const clearHistory = () => {
  uni.showModal({
    title: '提示',
    content: '确定要清空所有历史记录吗？',
    success: (res) => {
      if (res.confirm) {
        history.value = []
        uni.showToast({ title: '已清空' })
      }
    }
  })
}

const goToScan = () => {
  uni.switchTab({
    url: '/pages/scan/index'
  })
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString()
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
}

.title {
  font-size: 36rpx;
  color: #fff;
  font-weight: bold;
}

.history-list {
  margin: 20rpx;
}

.history-item {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.history-info {
  flex: 1;
}

.history-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10rpx;
}

.history-time {
  font-size: 24rpx;
  color: #999;
  display: block;
  margin-bottom: 8rpx;
}

.history-count {
  font-size: 24rpx;
  color: #666;
  display: block;
}

.arrow {
  font-size: 32rpx;
  color: #ccc;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 200rpx;
}

.empty-icon {
  width: 240rpx;
  height: 240rpx;
  margin-bottom: 40rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 40rpx;
}

.empty-btn {
  padding: 25rpx 80rpx;
  background: #409EFF;
  border-radius: 50rpx;
  font-size: 28rpx;
  color: #fff;
  margin-bottom: 20rpx;
}

.clear-btn {
  font-size: 28rpx;
  color: #F56C6C;
  padding: 20rpx;
}
</style>
