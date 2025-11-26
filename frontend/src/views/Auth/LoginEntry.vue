<template>
  <div class="login-entry">
    <h1>欢迎使用宿舍管理系统</h1>
    <div class="options">
      <button @click="goToStudentRegister">注册学生账户</button>
      <button @click="goToStudentLogin">学生登录</button>
      <button @click="goToAdminLogin">管理员登录</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToStudentRegister = () => {
  router.push('/student/register')
}

const goToStudentLogin = () => {
  router.push('/student/login')
}

const goToAdminLogin = () => {
  router.push('/admin/login')
}
</script>

<style scoped>
.login-entry {
  text-align: center;
  padding: 40px;
  font-family: Arial, sans-serif;
}

.options button {
  display: block;
  width: 200px;
  margin: 10px auto;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
}

.options button:hover {
  background: #0056b3;
}
</style>