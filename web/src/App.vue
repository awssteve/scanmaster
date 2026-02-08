<template>
  <div id="app">
    <el-container class="app-container">
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo">
            <el-icon :size="28" color="#409EFF">
              <Scan />
            </el-icon>
            <span class="logo-text">智扫通</span>
          </div>
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            @select="handleMenuSelect"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/scan">扫描</el-menu-item>
            <el-menu-item index="/id-card">证件</el-menu-item>
            <el-menu-item index="/batch">批量</el-menu-item>
            <el-menu-item index="/advanced">高级</el-menu-item>
            <el-menu-item index="/documents">文档</el-menu-item>
            <el-menu-item index="/history">历史</el-menu-item>
            <el-menu-item index="/login" v-if="!isLoggedIn">登录</el-menu-item>
            <el-menu-item v-else>用户</el-menu-item>
          </el-menu>
        </div>
      </el-header>

      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)
const isLoggedIn = ref(false) // TODO: 根据实际登录状态

const handleMenuSelect = (index: string) => {
  router.push(index)
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.app-header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  height: 60px !important;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
}

.logo-text {
  color: #333;
}

.app-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}
</style>
