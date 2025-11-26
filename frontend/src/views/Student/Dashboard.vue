<template>
  <div>
    <h2>欢迎，{{ studentStore.personal_info.data.name}}</h2>
    <nav class="student-nav">
      <router-link to="/student/dormitory">宿舍信息</router-link>
      <router-link to="/student/fees">费用概览</router-link>
      <router-link to="/student/maintenance">维修请求</router-link>
      <router-link to="/student/change-request">宿舍更换</router-link>
      <router-link to="/student/modify-info">修改个人信息</router-link>
      <button @click="handleLogout" class="logout-btn">登出</button>
    </nav>
  </div>
</template>

<script setup>
import { useStudentStore } from '@/store/student'
import { useRouter } from 'vue-router'

const studentStore = useStudentStore()
const router = useRouter()

const handleLogout = async () => {
  await studentStore.logout()
  router.push('/')
}
</script>

<style scoped>
.student-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 20px;
}

.student-nav a {
  padding: 10px 15px;
  background: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background 0.2s;
}

.student-nav a:hover {
  background: #0056b3;
}

.logout-btn {
  margin-top: 10px;
  padding: 10px 15px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #c82333;
}
</style>