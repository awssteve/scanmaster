<template>
  <view class="container">
    <view class="header">
      <text class="title">我的文档</text>
      <view class="header-btn" @tap="goToScan">
        <text class="btn-text">新建</text>
      </view>
    </view>

    <view class="document-list" v-if="documents.length > 0">
      <view
        class="document-item"
        v-for="(doc, index) in documents"
        :key="index"
        @tap="viewDocument(doc)"
      >
        <image :src="doc.thumbnail" class="doc-thumb" />
        <view class="doc-info">
          <text class="doc-name">{{ doc.name }}</text>
          <text class="doc-type">{{ doc.type }}</text>
          <text class="doc-time">{{ formatDate(doc.created_at) }}</text>
        </view>
        <view class="doc-actions">
          <view class="action-btn" @tap.stop="deleteDocument(doc)">删除</view>
        </view>
      </view>
    </view>

    <view class="empty" v-else>
      <image src="/static/empty.png" class="empty-icon" />
      <text class="empty-text">暂无文档</text>
      <view class="empty-btn" @tap="goToScan">开始扫描</view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const documents = ref([])

onMounted(() => {
  loadDocuments()
})

const loadDocuments = () => {
  // TODO: 从后端加载文档列表
  // 模拟数据
  documents.value = [
    {
      id: '1',
      name: '文档1.jpg',
      type: '扫描',
      thumbnail: '/static/doc-thumb.png',
      created_at: new Date().toISOString()
    }
  ]
}

const viewDocument = (doc) => {
  uni.navigateTo({
    url: `/pages/document-result/index?id=${doc.id}`
  })
}

const deleteDocument = (doc) => {
  uni.showModal({
    title: '提示',
    content: '确定要删除这个文档吗？',
    success: (res) => {
      if (res.confirm) {
        uni.showToast({ title: '删除成功' })
        loadDocuments()
      }
    }
  })
}

const goToScan = () => {
  uni.switchTab({
    url: '/pages/scan/index'
  })
}

const goBack = () => {
  uni.navigateBack()
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
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
  padding: 10rpx 30rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8rpx;
}

.btn-text {
  font-size: 28rpx;
  color: #fff;
}

.document-list {
  margin: 20rpx;
}

.document-item {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.doc-thumb {
  width: 120rpx;
  height: 120rpx;
  border-radius: 8rpx;
  background: #f5f7fa;
  margin-right: 20rpx;
}

.doc-info {
  flex: 1;
}

.doc-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10rpx;
}

.doc-type {
  font-size: 24rpx;
  color: #666;
  display: block;
  margin-bottom: 8rpx;
}

.doc-time {
  font-size: 24rpx;
  color: #999;
  display: block;
}

.doc-actions {
  margin-left: 20rpx;
}

.action-btn {
  padding: 15rpx 30rpx;
  background: #f5f7fa;
  border-radius: 8rpx;
  font-size: 24rpx;
  color: #666;
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
}
</style>
