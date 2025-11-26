<template>
  <div>
    <!-- 返回仪表盘按钮 -->
    <router-link to="/student/dashboard" class="back-to-dashboard">← 返回仪表盘</router-link>

    <h2>修改个人信息</h2>

    <!-- 加载中提示 -->
    <div v-if="studentStore.loading" class="loading">
      <p>正在加载个人信息...</p>
    </div>

    <!-- 显示当前用户信息（只读） -->
    <div v-else-if="studentStore.personal_info" class="current-info">
      <h3>当前信息</h3>
      <p><strong>学号：</strong>{{ studentStore.personal_info.data.student_id }}</p>
      <p><strong>姓名：</strong>{{ studentStore.personal_info.data.name }}</p>
      <p><strong>性别：</strong>{{ studentStore.personal_info.data.gender }}</p>
      <p><strong>专业：</strong>{{ studentStore.personal_info.data.major }}</p>
      <p><strong>宿舍号：</strong>{{ studentStore.personal_info.data.dormitory_no }}</p>
      <p><strong>邮箱：</strong>{{ studentStore.personal_info.data.email }}</p>
      <p><strong>电话号码：</strong>{{ studentStore.personal_info.data.phone_number }}</p>
    </div>

    <!-- 修改表单 -->
    <form @submit.prevent="handleModifyInfo" class="modify-form" v-if="studentStore.personal_info">
      <div>
        <label>姓名：</label>
        <input v-model="form.name" placeholder="请输入姓名" required />
      </div>
      <div>
        <label>性别：</label>
        <select v-model="form.gender" required>
          <option value="">请选择</option>
          <option value="男">男</option>
          <option value="女">女</option>
          <option value="其他">其他</option>
        </select>
      </div>
      <div>
        <label>专业：</label>
        <input v-model="form.major" placeholder="请输入专业" required />
      </div>
      <div>
        <label>邮箱：</label>
        <input v-model="form.email" type="email" placeholder="请输入邮箱" required />
      </div>
      <div>
        <label>电话号码：</label>
        <input v-model="form.phone_number" placeholder="请输入电话号码" required />
      </div>

      <div class="form-actions">
        <button type="submit">保存修改</button>
        <button type="button" @click="cancelEdit" class="cancel-btn">取消</button>
      </div>
    </form>

    <!-- 无数据提示 -->
    <div v-else class="no-data">
      <p>无法获取个人信息，请重试或联系管理员。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStudentStore } from '@/store/student'

const router = useRouter()
const studentStore = useStudentStore()

// 表单数据
const form = ref({
  name: '',
  gender: '',
  major: '',
  email: '',
  phone_number: ''
})

// 页面加载时，如果 Store 中没有个人信息，则自动获取
onMounted(async () => {
  if (!studentStore.personal_info) {
    await studentStore.fetchStudentInfo()
  }
  // 初始化表单
  initForm()
})

// 初始化表单数据（从 Store 获取）
const initForm = () => {
  if (studentStore.personal_info) {
    form.value.name = studentStore.personal_info.name || ''
    form.value.gender = studentStore.personal_info.gender || ''
    form.value.major = studentStore.personal_info.major || ''
    form.value.email = studentStore.personal_info.email || ''
    form.value.phone_number = studentStore.personal_info.phone_number || ''
  }
}

// 提交修改
const handleModifyInfo = async () => {
  try {
    await studentStore.modifyInfo(form.value) // ✅ 直接调用 Store 方法
    alert('修改成功')
    // 可选：刷新当前信息（Store 会自动更新）
    // await studentStore.fetchStudentInfo()
  } catch (error) {
    alert('修改失败：' + error.message)
  }
}

// 取消编辑（恢复原数据）
const cancelEdit = () => {
  initForm()
  alert('已取消修改')
}

// 当 Store 中的 personal_info 变化时，自动初始化表单
watch(() => studentStore.personal_info, (newVal) => {
  if (newVal) {
    initForm()
  }
}, { immediate: true })
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

.loading, .no-data {
  text-align: center;
  padding: 20px;
  color: #666;
}

.current-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #dee2e6;
}

.current-info h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #495057;
}

.current-info p {
  margin: 5px 0;
  color: #495057;
}

.modify-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.modify-form div {
  display: flex;
  align-items: center;
  gap: 10px;
}

.modify-form label {
  width: 80px;
  text-align: right;
  font-weight: bold;
}

.modify-form input,
.modify-form select {
  padding: 8px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  flex: 1;
  font-size: 14px;
}

.modify-form input:focus,
.modify-form select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.form-actions {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  margin-top: 20px;
}

.form-actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}

.form-actions button[type="submit"] {
  background: #007bff;
  color: white;
}

.form-actions button[type="submit"]:hover {
  background: #0056b3;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background: #5a6268;
}
</style>