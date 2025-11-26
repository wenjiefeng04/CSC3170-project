<template>
  <!-- 返回仪表盘按钮 -->
    <router-link to="/admin/dashboard" class="back-to-dashboard">← 返回仪表盘</router-link>
  <div class="students-page">
    <h2>所有学生账户</h2>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <p>正在加载学生数据...</p>
    </div>

    <!-- 数据加载失败 -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="fetchStudents">刷新</button>
    </div>

    <!-- 数据加载成功 -->
    <div v-else>
      <!-- 搜索框（可选） -->
      <div class="search-bar">
        <input v-model="searchQuery" placeholder="搜索学生ID或姓名..." @keyup.enter="filterStudents" />
        <button @click="filterStudents">搜索</button>
      </div>

      <!-- 学生列表表格 -->
      <table class="students-table">
        <thead>
          <tr>
            <th>学号</th>
            <th>姓名</th>
            <th>性别</th>
            <th>专业</th>
            <th>宿舍号</th>
            <th>邮箱</th>
            <th>电话</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in filteredStudents" :key="student.student_id">
            <td>{{ student.student_id }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.gender }}</td>
            <td>{{ student.major }}</td>
            <td>{{ student.dormitory_no || '未分配' }}</td>
            <td>{{ student.email }}</td>
            <td>{{ student.phone_number }}</td>
            <td>
              <button @click="openEditModal(student)">编辑</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页（可选）
      <div class="pagination" v-if="filteredStudents.length > 10">
        <button @click="prevPage">上一页</button>
        <span>第 {{ currentPage }} 页</span>
        <button @click="nextPage">下一页</button>
      </div> -->
      <div class="pagination">
        <button @click="prevPage">上一页</button>
        <span>第 {{ currentPage }} 页</span>
        <button @click="nextPage">下一页</button>
      </div>
    </div>

    <!-- 编辑学生信息弹窗 -->
    <div v-if="editingStudent" class="modal-overlay">
      <div class="modal-content">
        <h3>编辑学生信息</h3>
        <form @submit.prevent="saveStudentInfo">
          <div class="form-group">
            <label>学号：</label>
            <input type="text" v-model="editingStudent.student_id" disabled />
          </div>
          <div class="form-group">
            <label>姓名：</label>
            <input type="text" v-model="editingStudent.name" required />
          </div>
          <div class="form-group">
            <label>性别：</label>
            <select v-model="editingStudent.gender" required>
              <option value="男">男</option>
              <option value="女">女</option>
              <option value="其他">其他</option>
            </select>
          </div>
          <div class="form-group">
            <label>专业：</label>
            <input type="text" v-model="editingStudent.major" required />
          </div>
          <div class="form-group">
            <label>邮箱：</label>
            <input type="email" v-model="editingStudent.email" required />
          </div>
          <div class="form-group">
            <label>电话：</label>
            <input type="text" v-model="editingStudent.phone_number" required />
          </div>
          <div class="form-actions">
            <button type="submit">保存</button>
            <button type="button" @click="closeEditModal">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/store/admin'

const adminStore = useAdminStore()

// 状态
const loading = ref(false)
const error = ref('')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 10
const editingStudent = ref(null)

// 获取学生列表
const fetchStudents = async () => {
  loading.value = true
  error.value = ''
  try {
    await adminStore.fetchAllStudents()
  } catch (err) {
    error.value = err.message || '获取学生列表失败'
  } finally {
    loading.value = false
  }
}

// 过滤学生
const filteredStudents = computed(() => {
  if (!searchQuery.value) {
    return adminStore.students.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
  }
  const query = searchQuery.value.toLowerCase()
  return adminStore.students.filter(student =>
    student.student_id.toLowerCase().includes(query) ||
    student.name.toLowerCase().includes(query)
  ).slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
})

// 分页
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}
const nextPage = () => {
  if (currentPage.value * pageSize < adminStore.students.length) currentPage.value++
}

// 编辑学生
const openEditModal = (student) => {
  editingStudent.value = { ...student } // 深拷贝避免直接修改 store
}
const closeEditModal = () => {
  editingStudent.value = null
}

// 保存学生信息
const saveStudentInfo = async () => {
  try {
    await adminStore.modifyStudentAccount(editingStudent.value)
    await fetchStudents() // 刷新列表
    closeEditModal()
  } catch (err) {
    error.value = err.message || '保存失败'
  }
}

// 页面加载时获取数据
onMounted(() => {
  if (adminStore.students.length === 0) {
    fetchStudents()
  }
})
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
.students-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-bar input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-bar button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.students-table th,
.students-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.students-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.students-table tr:hover {
  background-color: #f5f5f5;
}

.students-table button {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.students-table button:hover {
  background-color: #5a6268;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.pagination span {
  line-height: 32px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.form-actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.form-actions button[type="submit"] {
  background-color: #007bff;
  color: white;
}

.form-actions button[type="button"] {
  background-color: #6c757d;
  color: white;
}

.form-actions button:hover {
  opacity: 0.9;
}
</style>