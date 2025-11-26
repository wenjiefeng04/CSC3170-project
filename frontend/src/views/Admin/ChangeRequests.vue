<template>
  <div class="container">
    <!-- 顶部：仪表盘按钮 + 刷新按钮 -->
    <div class="header">
      <router-link to="/admin/dashboard" class="back-to-dashboard">← 返回仪表盘</router-link>
      <button @click="fetchChangeRequests" class="refresh-btn">🔄 刷新请求列表</button>
    </div>

    <!-- 标题 -->
    <h2>宿舍更换请求管理</h2>

    <!-- 加载中提示 -->
    <div v-if="adminStore.loading" class="loading">
      <p>正在加载宿舍更换请求...</p>
    </div>

    <!-- 无请求提示 -->
    <div v-else-if="changeRequestsList.length === 0" class="no-requests">
      <p>暂无宿舍更换请求</p>
    </div>

    <!-- 请求列表 -->
    <div v-else class="requests-list">
      <div v-for="(req, index) in changeRequestsList" :key="req.request_id" class="request-item">
        <div class="request-header">
          <span class="student-id">学生ID：{{ req.student_id }}</span>
          <span class="status" :class="'status-' + req.status">{{ req.status }}</span>
        </div>
        <div class="request-details">
          <p><strong>旧宿舍：</strong>{{ req.old_dormitory_no }}</p>
          <p><strong>新宿舍：</strong>{{ req.new_dormitory_no }}</p>
          <p><strong>申请理由：</strong>{{ req.reason }}</p>
          <p><strong>申请时间：</strong>{{ req.created_at }}</p>
          <p v-if="req.approved_at"><strong>审批时间：</strong>{{ req.approved_at }}</p>
        </div>

        <!-- 审批按钮 -->
        <div class="approval-actions">
          <button 
            v-if="req.status === '待审批'" 
            @click="approveRequest(req.request_id, req.student_id)"
            class="approve-btn"
          >
            批准
          </button>
          <button 
            v-if="req.status === '待审批'" 
            @click="rejectRequest(req.request_id, req.student_id)"
            class="reject-btn"
          >
            拒绝
          </button>
        </div>
      </div>
    </div>

    <!-- 右侧：可选宿舍 + 空床位数（仅开发环境） -->
    <div v-if="isDev && availableDormitories.length > 0" class="available-dorms-sidebar">
      <h3>可选宿舍 </h3>
      <ul>
        <li v-for="dorm in availableDormitories" :key="dorm.dormitory_no">
          {{ dorm.dormitory_no }} （空床：{{ dorm.available_beds }}）
        </li>
      </ul>
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

// 是否为开发环境
const isDev = import.meta.env.DEV // ✅ Vite 环境变量

// 计算属性：获取请求列表
const changeRequestsList = computed(() => {
  if (!adminStore.changeRequests?.data?.dormitory_change_requests) {
    return []
  }
  // ✅ 直接返回后端已排序的数据
  return adminStore.changeRequests.data.dormitory_change_requests
})

// 计算属性：获取可选宿舍
const availableDormitories = computed(() => {
  if (!adminStore.changeRequests?.data?.avaliable_dormitories) {
    return []
  }
  return adminStore.changeRequests.data.avaliable_dormitories
})

// 刷新请求
const fetchChangeRequests = async () => {
  try {
    await adminStore.fetchAllChangeRequests()
    // 清除消息
    message.value = null
  } catch (error) {
    message.value = {
      type: 'error',
      text: '加载请求失败：' + error.message
    }
    setTimeout(() => {
      message.value = null
    }, 3000)
  }
}

// 批准请求
const approveRequest = async (requestId, studentId) => {
  try {
    await adminStore.approveChangeRequest({
      request_id: requestId,
      student_id: studentId,
      action: 'approve'
    })
    message.value = {
      type: 'success',
      text: '请求已批准'
    }
    setTimeout(() => {
      message.value = null
    }, 3000)
  } catch (error) {
    message.value = {
      type: 'error',
      text: '批准失败：' + error.message
    }
    setTimeout(() => {
      message.value = null
    }, 3000)
  }
}

// 拒绝请求
const rejectRequest = async (requestId, studentId) => {
  try {
    await adminStore.approveChangeRequest({
      request_id: requestId,
      student_id: studentId,
      action: 'reject'
    })
    message.value = {
      type: 'success',
      text: '请求已拒绝'
    }
    setTimeout(() => {
      message.value = null
    }, 3000)
  } catch (error) {
    message.value = {
      type: 'error',
      text: '拒绝失败：' + error.message
    }
    setTimeout(() => {
      message.value = null
    }, 3000)
  }
}

// 页面加载时获取请求
onMounted(() => {
  fetchChangeRequests()
})
</script>

<style scoped>
.container {
  padding: 20px;
  position: relative; /* 为侧边栏定位提供参考 */
}

.header {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.back-to-dashboard {
  display: inline-block;
  padding: 8px 16px;
  background: #6c757d;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background 0.2s;
}

.back-to-dashboard:hover {
  background: #5a6268;
  text-decoration: none;
}

.refresh-btn {
  align-self: flex-start;
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}

.refresh-btn:hover {
  background: #0056b3;
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.loading, .no-requests {
  text-align: center;
  padding: 20px;
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

.status-待审批 {
  background: #fff3cd;
  color: #856404;
}

.status-已批准 {
  background: #d4edda;
  color: #155724;
}

.status-已拒绝 {
  background: #f8d7da;
  color: #721c24;
}

.request-details {
  font-size: 0.9em;
  color: #666;
  line-height: 1.5;
}

.approval-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.approve-btn {
  background: #28a745;
  color: white;
}

.approve-btn:hover {
  background: #218838;
}

.reject-btn {
  background: #dc3545;
  color: white;
}

.reject-btn:hover {
  background: #c82333;
}

/* 右侧：可选宿舍 + 空床位数 */
.available-dorms-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 250px;
  height: 100vh;
  background: #f8f9fa;
  border-left: 1px solid #dee2e6;
  padding: 20px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: -2px 0 5px rgba(0,0,0,0.1);
}

.available-dorms-sidebar h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #495057;
  font-size: 1.1em;
}

.available-dorms-sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.available-dorms-sidebar li {
  margin: 5px 0;
  color: #495057;
  padding: 8px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 4px;
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