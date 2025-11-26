<template>
  <div class="admin-dashboard">
    <!-- 顶部个人信息栏 -->
    <header class="info-header">
      <div class="personal-info">
        <h2>管理员信息</h2>
        <div class="info-row">
          <span class="label">姓名：</span>
          <span class="value">{{ adminStore.admin_info?.name || '加载中...' }}</span>
        </div>
        <div class="info-row">
          <span class="label">管理员ID：</span>
          <span class="value">{{ adminStore.admin_info?.admin_id || '-' }}</span>
        </div>
        <div class="info-row">
          <span class="label">邮箱：</span>
          <span class="value">{{ adminStore.admin_info?.email || '-' }}</span>
        </div>
        <div class="info-row">
          <span class="label">电话：</span>
          <span class="value">{{ adminStore.admin_info?.phone_number || '-' }}</span>
        </div>
        <div class="info-row">
          <span class="label">账户创建时间：</span>
          <span class="value">{{ formatDate(adminStore.admin_info?.created_at) || '-' }}</span>
        </div>
        <button class="edit-btn" @click="showModifyModal = true">
          ✏️ 修改信息
        </button>
      </div>
      <button class="logout-btn" @click="handleLogout">登出</button>
    </header>

    <!-- 导航菜单 -->
    <nav class="admin-nav">
      <router-link to="/admin/students" class="nav-item">管理学生</router-link>
      <router-link to="/admin/change-requests" class="nav-item">审批更换请求</router-link>
      <router-link to="/admin/dormitory-status" class="nav-item">宿舍状态</router-link>
      <router-link to="/admin/maintenance" class="nav-item">处理维修请求</router-link>
    </nav>

    <!-- 主内容区 -->
    <main class="admin-content">
      <slot />
    </main>

    <!-- 修改信息弹窗 -->
    <div v-if="showModifyModal" class="modal-overlay">
      <div class="modal">
        <h3>修改个人信息</h3>
        <form @submit.prevent="handleModify">
          <div class="form-group">
            <label>姓名：</label>
            <input 
              v-model="form.name" 
              required 
              placeholder="请输入姓名"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label>邮箱：</label>
            <input 
              v-model="form.email" 
              type="email" 
              required 
              placeholder="请输入邮箱"
              class="form-control"
            />
            <span v-if="!isEmailValid" class="error-text">请输入有效的邮箱格式</span>
          </div>
          <div class="form-group">
            <label>电话：</label>
            <input 
              v-model="form.phone_number" 
              required 
              placeholder="请输入电话号码"
              class="form-control"
            />
            <span v-if="!isPhoneValid" class="error-text">请输入有效的电话号码（11位数字）</span>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showModifyModal = false" class="cancel-btn">取消</button>
            <button type="submit" class="submit-btn" :disabled="!isFormValid">保存修改</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAdminStore } from '@/store/admin'
import { useRouter } from 'vue-router'

const adminStore = useAdminStore()
const router = useRouter()

// 状态管理
const showModifyModal = ref(false)
const form = ref({
  name: '',
  email: '',
  phone_number: ''
})
const isEmailValid = ref(true)
const isPhoneValid = ref(true)

// 初始化个人信息
onMounted(async () => {
  await adminStore.fetchAdminInfo()
})

// 监听用户信息变化，同步到表单
// watch(
//   () => adminStore.user,
//   (newUser) => {
//     if (newUser) {
//       form.value = {
//         name: newUser.name || '',
//         email: newUser.email || '',
//         phone_number: newUser.phone_number || ''
//       }
//     }
//   },
//   { immediate: true }
// )
watch(
  () => showModifyModal.value,
  (newVal) => {
    if (newVal && adminStore.admin_info) {
      // 从 admin_info 读取数据（而非 user）
      form.value = {
        name: adminStore.admin_info.name || '',
        email: adminStore.admin_info.email || '',
        phone_number: adminStore.admin_info.phone_number || ''
      }
      // 重置验证状态
      isEmailValid.value = true
      isPhoneValid.value = true
    }
  }
)

// 表单验证
const isFormValid = computed(() => {
  validateEmail()
  validatePhone()
  return isEmailValid.value && isPhoneValid.value && form.value.name.trim()
})

// 邮箱验证
const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  isEmailValid.value = emailRegex.test(form.value.email)
}

// 电话验证
const validatePhone = () => {
  const phoneRegex = /^1[3-9]\d{9}$/
  isPhoneValid.value = phoneRegex.test(form.value.phone_number)
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 处理修改信息
const handleModify = async () => {
  try {
    await adminStore.modifyOwnInfo(form.value)
    showModifyModal.value = false
    alert('信息修改成功！')
  } catch (error) {
    alert('修改失败：' + error.message)
  }
}

// 处理登出
const handleLogout = async () => {
  await adminStore.logout()
  router.push('/')
}
</script>

<style scoped>
/* 基础样式 */
.admin-dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

/* 头部信息区 */
.info-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.personal-info {
  flex: 1;
  min-width: 300px;
}

.personal-info h2 {
  margin-top: 0;
  margin-bottom: 16px;
  color: #2c3e50;
  border-bottom: 2px solid #007bff;
  padding-bottom: 8px;
}

.info-row {
  display: flex;
  margin-bottom: 10px;
  line-height: 1.6;
}

.label {
  width: 120px;
  font-weight: 600;
  color: #495057;
}

.value {
  flex: 1;
  color: #2d3436;
}

.edit-btn {
  margin-top: 16px;
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.edit-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

.logout-btn {
  padding: 8px 16px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  margin-left: 20px;
  align-self: flex-start;
}

.logout-btn:hover {
  background: #c82333;
}

/* 导航菜单 */
.admin-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}

.nav-item {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s;
  flex-shrink: 0;
}

.nav-item:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

.nav-item.router-link-active {
  background: #0056b3;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.3);
}

/* 主内容区 */
.admin-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  min-height: 400px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

/* 修改信息弹窗 */
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
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.modal h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
}

.form-group {
  margin-bottom: 16px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0,123,255,0.2);
}

.error-text {
  color: #dc3545;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 24px;
}

.cancel-btn {
  padding: 8px 16px;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.cancel-btn:hover {
  background: #5a6268;
}

.submit-btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.submit-btn:not(:disabled):hover {
  background: #0056b3;
}
</style>