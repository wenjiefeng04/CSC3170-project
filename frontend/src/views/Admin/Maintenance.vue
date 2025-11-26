<template>
  <div class="container">
    <!-- 返回仪表盘按钮 -->
    <router-link to="/admin/dashboard" class="back-to-dashboard">← 返回仪表盘</router-link>

    <h2>维修请求管理</h2>

    <!-- 刷新按钮 -->
    <button @click="fetchMaintenanceRequests" class="refresh-btn">🔄 刷新请求列表</button>

    <!-- 加载中提示 -->
    <div v-if="adminStore.loading" class="loading">
      <p>正在加载维修请求...</p>
    </div>

    <!-- 无请求提示 -->
    <div v-else-if="maintenanceRequestsList.length === 0" class="no-requests">
      <p>暂无维修请求</p>
    </div>

    <!-- 请求列表 -->
    <div v-else class="requests-list">
      <div v-for="req in maintenanceRequestsList" :key="req.request_id" class="request-item">
        <div class="request-header">
          <span class="student-id">学生ID：{{ req.student_id }}</span>
          <span class="status" :class="'status-' + req.status">{{ req.status }}</span>
        </div>
        <div class="request-details">
          <p><strong>问题描述：</strong>{{ req.issue }}</p>
          <p><strong>优先级：</strong>{{ req.priority }}</p>
          <p><strong>提交时间：</strong>{{ req.created_at }}</p>
          <p v-if="req.resolved_at"><strong>处理时间：</strong>{{ req.resolved_at }}</p>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button 
            v-if="req.status === '待处理'" 
            @click="processRequest(req.request_id, '处理中')"
            class="process-btn"
          >
            标记为处理中
          </button>
          <button 
            v-if="req.status === '处理中'" 
            @click="processRequest(req.request_id, '已完成')"
            class="complete-btn"
          >
            标记为已完成
          </button>
        </div>
      </div>
    </div>

    <!-- 消息提示 -->
    <div v-if="message" :class="{'success-msg': message.type === 'success', 'error-msg': message.type === 'error'}">
      {{ message.text }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/store/admin'

const adminStore = useAdminStore()

// 消息状态
const message = ref(null)

// 计算属性：获取维修请求列表
const maintenanceRequestsList = computed(() => {
  if (!adminStore.maintenanceRequests?.data?.maintenance_requests) {
    return []
  }
  return adminStore.maintenanceRequests.data.maintenance_requests
})

// 刷新请求列表
const fetchMaintenanceRequests = async () => {
  try {
    adminStore.loading = true
    await adminStore.fetchAllMaintenanceRequests()
    message.value = null
  } catch (error) {
    message.value = {
      type: 'error',
      text: '加载失败：' + error.message
    }
    setTimeout(() => {
      message.value = null
    }, 3000)
  } finally {
    adminStore.loading = false
  }
}

// 处理维修请求
const processRequest = async (requestId, action) => {
  try {
    await adminStore.processMaintenanceRequest({
      request_id: requestId,
      action: action
    })
    message.value = {
      type: 'success',
      text: `请求已${action}`
    }
    setTimeout(() => {
      message.value = null
    }, 3000)
  } catch (error) {
    message.value = {
      type: 'error',
      text: '操作失败：' + error.message
    }
    setTimeout(() => {
      message.value = null
    }, 3000)
  }
}

// 页面加载时获取请求
onMounted(() => {
  fetchMaintenanceRequests()
})
</script>

<style scoped>
.container {
  padding: 20px;
}

.back-to-dashboard {
  display: inline-block;
  margin-bottom: 15px;
  padding: 8px 16px;
  background: #6c757d;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
}

.back-to-dashboard:hover {
  background: #5a6268;
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.refresh-btn {
  margin-bottom: 20px;
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.refresh-btn:hover {
  background: #0056b3;
}

.loading, .no-requests {
  text-align: center;
  padding: 40px 0;
  color: #666;
}

.requests-list {
  margin-top: 20px;
}

.request-item {
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  margin: 10px 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.student-id {
  font-weight: bold;
  flex: 1;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: bold;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-处理中 {
  background: #d1ecf1;
  color: #0c5460;
}

.status-已完成 {
  background: #d4edda;
  color: #155724;
}

.request-details {
  font-size: 0.9em;
  color: #666;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.process-btn {
  background: #17a2b8;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.process-btn:hover {
  background: #138496;
}

.complete-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.complete-btn:hover {
  background: #218838;
}

.success-msg {
  background: #d4edda;
  color: #155724;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
  border: 1px solid #c3e6cb;
}

.error-msg {
  background: #f8d7da;
  color: #721c24;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
  border: 1px solid #f5c6cb;
}
</style>