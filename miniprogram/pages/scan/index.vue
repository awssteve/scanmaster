<template>
  <view class="container">
    <camera
      class="camera"
      :device-position="devicePosition"
      :flash="flash"
      @ready="onCameraReady"
      @stop="onCameraStop"
    />

    <!-- 顶部工具栏 -->
    <view class="toolbar">
      <view class="toolbar-item" @tap="toggleCamera">
        <image src="/static/flip.png" class="toolbar-icon" />
      </view>
      <view class="toolbar-item" @tap="toggleFlash">
        <image src="/static/flash.png" class="toolbar-icon" />
      </view>
    </view>

    <!-- 底部操作栏 -->
    <view class="bottom-bar">
      <view class="bottom-item" @tap="goBack">
        <text class="bottom-text">取消</text>
      </view>

      <view class="bottom-item center" @tap="takePhoto">
        <view class="shutter-btn"></view>
      </view>

      <view class="bottom-item" @tap="goToAlbum">
        <image src="/static/album.png" class="album-icon" />
        <text class="bottom-text">相册</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const devicePosition = ref('back')
const flash = ref('off')

const onCameraReady = (e) => {
  console.log('Camera ready', e)
}

const onCameraStop = (e) => {
  console.log('Camera stop', e)
}

const toggleCamera = () => {
  devicePosition.value = devicePosition.value === 'back' ? 'front' : 'back'
}

const toggleFlash = () => {
  const flashOptions = ['off', 'on', 'auto', 'torch']
  const currentIndex = flashOptions.indexOf(flash.value)
  flash.value = flashOptions[(currentIndex + 1) % flashOptions.length]
}

const takePhoto = () => {
  uni.createCameraContext().takePhoto({
    quality: 'high',
    success: (res) => {
      console.log('Photo taken', res)
      // 跳转到扫描结果页
      uni.navigateTo({
        url: `/pages/scan-result/index?tempFilePath=${res.tempImagePath}`
      })
    },
    fail: (err) => {
      uni.showToast({
        title: '拍照失败',
        icon: 'none'
      })
    }
  })
}

const goToAlbum = () => {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album'],
    success: (res) => {
      const tempFilePath = res.tempFilePaths[0]
      uni.navigateTo({
        url: `/pages/scan-result/index?tempFilePath=${tempFilePath}`
      })
    }
  })
}

const goBack = () => {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.container {
  position: relative;
  width: 100%;
  height: 100vh;
}

.camera {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.toolbar {
  position: absolute;
  top: 40rpx;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  padding: 0 40rpx;
}

.toolbar-item {
  width: 80rpx;
  height: 80rpx;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toolbar-icon {
  width: 48rpx;
  height: 48rpx;
}

.bottom-bar {
  position: absolute;
  bottom: 80rpx;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 0 60rpx;
}

.bottom-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bottom-item.center {
  width: 160rpx;
  height: 160rpx;
  border-radius: 50%;
  border: 6rpx solid #fff;
  background: rgba(255, 255, 255, 0.2);
}

.shutter-btn {
  width: 120rpx;
  height: 120rpx;
  background: #fff;
  border-radius: 50%;
  margin: 20rpx;
}

.album-icon {
  width: 48rpx;
  height: 48rpx;
  margin-bottom: 8rpx;
}

.bottom-text {
  font-size: 24rpx;
  color: #fff;
  margin-top: 8rpx;
}
</style>
