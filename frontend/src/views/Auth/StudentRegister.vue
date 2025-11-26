<template>
  <div>
    <h2>学生注册</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="form.student_id" placeholder="学生ID" required />
      <input v-model="form.password" type="password" placeholder="密码" required />
      <input v-model="form.name" placeholder="用户名" required />
      <input v-model="form.gender" placeholder="性别" required />
      <input v-model="form.major" placeholder="专业" required />
      <input v-model="form.email" placeholder="邮箱" required />
      <input v-model="form.phone_number" placeholder="电话号码" required />
      <button type="submit">注册</button>
    </form>
    <p><router-link to="/student/login">已有账号？去登录</router-link></p>
    <p><router-link to="/">返回首页</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import studentApi from '@/api/student'

const router = useRouter()

const form = ref({
  major: '',
  password: '',
  name: '',
  student_id: '',
  email: '',
  gender: ''
})

const handleRegister = async () => {
  try {
    await studentApi.register(form.value)
    alert('注册成功，请登录')
    router.push('/student/login')
  } catch (error) {
    // alert('注册失败')
    // 从 error.response.data 中提取后端返回的错误信息
    const errorMessage = error.response?.data?.message || '注册失败，请重试'
    alert(errorMessage)
  }
}
</script>