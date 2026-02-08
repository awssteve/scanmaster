<template>
  <div class="history">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>扫描历史</span>
          <el-button @click="clearHistory" link type="danger">清空历史</el-button>
        </div>
      </template>

      <el-empty v-if="history.length === 0" description="暂无历史记录" />

      <el-timeline v-else>
        <el-timeline-item
          v-for="item in history"
          :key="item.id"
          :timestamp="item.timestamp"
          placement="top"
        >
          <el-card>
            <h4>{{ item.name }}</h4>
            <p>识别文字数：{{ item.textCount }}</p>
            <el-button link type="primary" @click="viewResult(item.id)">
              查看详情
            </el-button>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

interface HistoryItem {
  id: string
  name: string
  timestamp: string
  textCount: number
}

const history = ref<HistoryItem[]>([])

const clearHistory = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有历史记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    history.value = []
    ElMessage.success('历史记录已清空')
  } catch (error) {
    // 用户取消
  }
}

const viewResult = (id: string) => {
  router.push(`/result/${id}`)
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-card h4 {
  margin: 0 0 10px;
  color: #333;
}

.el-card p {
  margin: 0 0 10px;
  color: #666;
  font-size: 14px;
}
</style>
