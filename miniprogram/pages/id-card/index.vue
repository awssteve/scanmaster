<template>
  <view class="container">
    <view class="header">
      <text class="title">证件扫描</text>
    </view>

    <!-- 证件类型选择 -->
    <scroll-view class="card-list" scroll-y>
      <view
        class="card-item"
        v-for="(card, index) in cardTypes"
        :key="index"
        @tap="selectCard(card)"
      >
        <image :src="card.icon" class="card-icon" />
        <view class="card-info">
          <text class="card-name">{{ card.name }}</text>
          <text class="card-desc">{{ card.desc }}</text>
        </view>
        <text class="arrow">></text>
      </view>
    </scroll-view>

    <!-- 底部操作栏 -->
    <view class="bottom-bar">
      <view class="bottom-item" @tap="goBack">
        <text class="bottom-text">返回</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const cardTypes = ref([
  {
    type: 'id_card',
    name: '身份证',
    desc: '中国大陆身份证',
    icon: '/static/id-card.png'
  },
  {
    type: 'passport',
    name: '护照',
    desc: '中国护照',
    icon: '/static/passport.png'
  },
  {
    type: 'license',
    name: '驾驶证',
    desc: '机动车驾驶证',
    icon: '/static/license.png'
  },
  {
    type: 'graduation',
    name: '毕业证',
    desc: '毕业证书',
    icon: '/static/graduation.png'
  },
  {
    type: 'student_card',
    name: '学生证',
    desc: '学生证件',
    icon: '/static/student-card.png'
  }
])

const selectCard = (card) => {
  uni.navigateTo({
    url: `/pages/id-card-scan/index?type=${card.type}&name=${card.name}`
  })
}

const goBack = () => {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 120rpx;
}

.header {
  background: #409EFF;
  padding: 40rpx;
}

.title {
  font-size: 36rpx;
  color: #fff;
  font-weight: bold;
}

.card-list {
  margin-top: 20rpx;
  height: calc(100vh - 160rpx);
}

.card-item {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin: 0 20rpx 20rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.card-icon {
  width: 80rpx;
  height: 80rpx;
  margin-right: 20rpx;
}

.card-info {
  flex: 1;
}

.card-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10rpx;
}

.card-desc {
  font-size: 24rpx;
  color: #999;
  display: block;
}

.arrow {
  font-size: 32rpx;
  color: #ccc;
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 20rpx 40rpx;
  box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: center;
}

.bottom-item {
  width: 100%;
}

.bottom-text {
  font-size: 28rpx;
  color: #409EFF;
  text-align: center;
  display: block;
}
</style>
