<template>
  <div>
    <!-- 返回仪表盘按钮 -->
    <router-link to="/student/dashboard" class="back-to-dashboard">← 返回仪表盘</router-link>

    <h2>宿舍更换请求</h2>

    <!-- 提交新请求 -->
    <div class="submit-section">
      <h3>提交新宿舍更换请求</h3>
      <form @submit.prevent="submitRequest">
        <div>
          <label>新宿舍号：</label>
          <input v-model="form.new_dormitory_no" placeholder="如：5" required />
        </div>
        <div>
          <label>更换理由：</label>
          <textarea v-model="form.reason" placeholder="请说明更换宿舍的原因" required rows="3"></textarea>
        </div>
        <button type="submit">提交请求</button>
      </form>
    </div>

    <!-- 所有更换请求列表 -->
    <div class="requests-section">
      <h3>我的所有宿舍更换请求</h3>

      <!-- 加载中 -->
      <div v-if="!studentStore.changeRequests" class="loading">
        <p>正在加载宿舍更换请求...</p>
      </div>

      <!-- 数据加载成功 -->
      <div v-else>
        <!-- 如果没有请求 -->
        <div v-if="changeRequestsList.length === 0" class="no-requests">
          <p>暂无宿舍更换请求</p>
        </div>

        <!-- 如果有请求 -->
        <ul v-else class="requests-list">
          <li v-for="(req, index) in changeRequestsList" :key="req.request_id || index" class="request-item">
            <div class="request-header">
              <span class="issue">从 {{ req.old_dormitory_no }} → {{ req.new_dormitory_no }}</span>
              <span class="status" :class="'status-' + req.status">{{ req.status }}</span>
            </div>
            <div class="request-details">
              <p><strong>更换理由：</strong>{{ req.reason }}</p>
              <p><strong>创建时间：</strong>{{ req.created_at }}</p>
              <p v-if="req.approved_at"><strong>批准时间：</strong>{{ req.approved_at }}</p>
            </div>
            <!-- 修改按钮（仅限 pending 状态） -->
            <button 
              v-if="req.status === '待审批'" 
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
        <h4>修改宿舍更换请求 #{{ editingRequest.request_id }}</h4>
        <form @submit.prevent="saveEdit">
          <div>
            <label>新宿舍号：</label>
            <input v-model="editingForm.new_dormitory_no" placeholder="如：A301" required />
          </div>
          <div>
            <label>更换理由：</label>
            <textarea v-model="editingForm.reason" placeholder="请说明更换宿舍的原因" required rows="3"></textarea>
          </div>
          <div class="modal-actions">
            <button type="submit">保存修改</button>
            <button type="button" @click="cancelEdit">取消</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 刷新按钮 -->
    <button @click="fetchChangeRequests" class="refresh-btn">🔄 刷新列表</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStudentStore } from '@/store/student'
import studentApi from '@/api/student'

const studentStore = useStudentStore()

// 表单数据 - 新请求
const form = ref({
  new_dormitory_no: '',
  reason: ''
})

// 编辑状态
const editingRequest = ref(null)
const editingForm = ref({
  new_dormitory_no: '',
  reason: '',
  request_id: null
})

// 计算属性：获取更换请求列表
const changeRequestsList = computed(() => {
  if (!studentStore.changeRequests?.data?.dormitory_change_requests) {
    return []
  }
  return studentStore.changeRequests.data.dormitory_change_requests
})

// 提交新请求
const submitRequest = async () => {
  try {
    await studentApi.submitChangeRequest(form.value)
    await studentStore.fetchChangeRequests()
    form.value.new_dormitory_no = ''
    form.value.reason = ''
    alert('提交成功')
  } catch (error) {
    alert('提交失败：' + error.message)
  }
}

// 开始编辑
const startEditing = (request) => {
  editingRequest.value = request
  editingForm.value = {
    new_dormitory_no: request.new_dormitory_no,
    reason: request.reason,
    request_id: request.request_id
  }
}

// 取消编辑
const cancelEdit = () => {
  editingRequest.value = null
  editingForm.value = {
    new_dormitory_no: '',
    reason: '',
    request_id: null
  }
}

// 保存修改
const saveEdit = async () => {
  try {
    await studentApi.modifyChangeRequest(editingForm.value)
    await studentStore.fetchChangeRequests()
    cancelEdit()
    alert('修改成功')
  } catch (error) {
    alert('修改失败：' + error.message)
  }
}

// 刷新请求
const fetchChangeRequests = async () => {
  await studentStore.fetchChangeRequests()
}
</script>

<style scoped>
.back-to-dashboard {
  display: inline-block;
  margin-bottom: 15px;
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

form input, form textarea {
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

.status-approved {
  background: #d4edda;
  color: #155724;
}

.status-rejected {
  background: #f8d7da;
  color: #721c24;
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