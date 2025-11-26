<template>
  <div>
    <router-link to="/student/dashboard" class="back-to-dashboard">← 返回仪表盘</router-link>
    <h2>维修请求管理</h2>

    <!-- 提交新请求 -->
    <div class="submit-section">
      <h3>提交新维修请求</h3>
      <form @submit.prevent="submitRequest">
        <div>
          <label>问题描述：</label>
          <input v-model="form.issue" placeholder="请详细描述问题" required />
        </div>
        <div>
          <label>优先级：</label>
          <select v-model="form.priority" required>
            <option value="低">低</option>
            <option value="中">中</option>
            <option value="高">高</option>
          </select>
        </div>
        <button type="submit">提交请求</button>
      </form>
    </div>

    <!-- 所有维修请求列表 -->
    <div class="requests-section">
      <h3>我的所有维修请求</h3>

      <!-- 加载中 -->
      <div v-if="!studentStore.maintenanceRequests" class="loading">
        <p>正在加载维修请求...</p>
      </div>

      <!-- 数据加载成功 -->
      <div v-else>
        <!-- 如果没有请求 -->
        <div v-if="maintenanceRequestsList.length === 0" class="no-requests">
          <p>暂无维修请求</p>
        </div>

        <!-- 如果有请求 -->
        <ul v-else class="requests-list">
          <li v-for="(req, index) in maintenanceRequestsList" :key="req.request_id || index" class="request-item">
            <div class="request-header">
              <span class="issue">{{ req.issue }}</span>
              <span class="status" :class="'status-' + req.status">{{ req.status }}</span>
            </div>
            <div class="request-details">
              <p><strong>宿舍号：</strong>{{ req.dormitory_no }}</p>
              <p><strong>优先级：</strong>{{ req.priority }}</p>
              <p><strong>创建时间：</strong>{{ req.created_at }}</p>
              <p v-if="req.resolved_at"><strong>解决时间：</strong>{{ req.resolved_at }}</p>
            </div>
            <!-- 修改按钮（仅限 待处理 状态） -->
            <button 
              v-if="req.status === '待处理'" 
              @click="startEditing(req)"
              class="edit-btn"
            >
              修改
            </button>
          </li>
        </ul>
      </div>
    </div>

    <!-- 修改请求的弹窗 -->
    <div v-if="editingRequest" class="modal-overlay">
      <div class="modal">
        <h4>修改维修请求 #{{ editingRequest.request_id }}</h4>
        <form @submit.prevent="saveEdit">
          <div>
            <label>问题描述：</label>
            <input v-model="editingForm.issue" placeholder="请详细描述问题" required />
          </div>
          <div>
            <label>优先级：</label>
            <select v-model="editingForm.priority" required>
              <option value="低">低</option>
              <option value="中">中</option>
              <option value="高">高</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="submit">保存修改</button>
            <button type="button" @click="cancelEdit">取消</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 刷新按钮 -->
    <button @click="fetchMaintenanceRequests" class="refresh-btn">🔄 刷新列表</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStudentStore } from '@/store/student'

const studentStore = useStudentStore()
import studentApi from '@/api/student'

// 表单数据 - 新请求
const form = ref({
  issue: '',
  priority: 'medium'
})

// 编辑状态
const editingRequest = ref(null)
const editingForm = ref({
  issue: '',
  priority: 'medium',
  request_id: null
})

// 计算属性：获取维修请求列表
const maintenanceRequestsList = computed(() => {
  if (!studentStore.maintenanceRequests?.data?.maintenance_requests) {
    return []
  }
  return studentStore.maintenanceRequests.data.maintenance_requests
})

// 提交新请求
const submitRequest = async () => {
  try {
    await studentApi.submitMaintenanceRequest(form.value)
    await studentStore.fetchMaintenanceRequests()
    form.value.issue = ''
    form.value.priority = '中'
    alert('提交成功')
  } catch (error) {
    alert('提交失败：' + error.message)
  }
}

// 开始编辑
const startEditing = (request) => {
  editingRequest.value = request
  editingForm.value = {
    issue: request.issue,
    priority: request.priority,
    request_id: request.request_id
  }
}

// 取消编辑
const cancelEdit = () => {
  editingRequest.value = null
  editingForm.value = {
    issue: '',
    priority: 'medium',
    request_id: null
  }
}

// 保存修改
const saveEdit = async () => {
  try {
    await studentApi.modifyMaintenanceRequest(editingForm.value)
    await studentStore.fetchMaintenanceRequests()
    cancelEdit()
    alert('修改成功')
  } catch (error) {
    alert('修改失败：' + error.message)
  }
}

// 刷新请求
const fetchMaintenanceRequests = async () => {
  await studentStore.fetchMaintenanceRequests()
}
</script>

<style scoped>
.submit-section, .requests-section {
  margin: 20px 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

form div {
  display: flex;
  align-items: center;
  gap: 10px;
}

form label {
  width: 80px;
  text-align: right;
}

form input, form select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  flex: 1;
}

button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #0056b3;
}

.requests-list {
  list-style: none;
  padding: 0;
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

.issue {
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

.status-completed {
  background: #d4edda;
  color: #155724;
}

.status-resolved {
  background: #d1ecf1;
  color: #0c5460;
}

.request-details {
  font-size: 0.9em;
  color: #666;
  line-height: 1.5;
}

.edit-btn {
  background: #ffc107;
  color: #212529;
  margin-left: 10px;
}

.edit-btn:hover {
  background: #e0a800;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}

.modal h4 {
  margin-top: 0;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.modal-actions button {
  flex: 1;
  margin: 0 5px;
}

.refresh-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.refresh-btn:hover {
  background: #5a6268;
}

.loading, .no-requests {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>