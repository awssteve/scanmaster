<template>
  <div class="documents">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的文档</span>
          <el-button type="primary" @click="goToScan">新建扫描</el-button>
        </div>
      </template>

      <el-empty v-if="documents.length === 0" description="暂无文档" />

      <el-table :data="documents" v-else>
        <el-table-column prop="name" label="文档名称" />
        <el-table-column prop="type" label="类型">
          <template #default="{ row }">
            <el-tag>{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button link type="primary" @click="viewDocument(row)">
              查看
            </el-button>
            <el-button link type="danger" @click="deleteDocument(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getDocuments, type Document } from '@/api'

const router = useRouter()
const documents = ref<Document[]>([])

const loadDocuments = async () => {
  try {
    const data = await getDocuments()
    documents.value = data
  } catch (error) {
    ElMessage.error('加载文档失败')
  }
}

const goToScan = () => {
  router.push('/scan')
}

const viewDocument = (document: Document) => {
  router.push(`/result/${document.id}`)
}

const deleteDocument = async (document: Document) => {
  try {
    await ElMessageBox.confirm('确定要删除这个文档吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    ElMessage.success('删除成功')
    loadDocuments()
  } catch (error) {
    // 用户取消
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    success: 'success',
    processing: 'warning',
    failed: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    success: '已完成',
    processing: '处理中',
    failed: '失败'
  }
  return map[status] || status
}

onMounted(() => {
  loadDocuments()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
