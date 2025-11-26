<template>
  <div>
    <h2>学生登录</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="form.student_id" placeholder="学生ID" required />
      <input v-model="form.password" type="password" placeholder="密码" required />
      <button type="submit">登录</button>
    </form>
    <p><router-link to="/">返回首页</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import studentApi from '@/api/student'
import { useStudentStore } from '@/store/student'

const router = useRouter()
const studentStore = useStudentStore()

const form = ref({
  student_id: '',
  password: ''
})

const handleLogin = async () => {
  try {
    const message = await studentStore.login(form.value)
    alert(message)
    router.push('/student/dashboard')
  } catch (error) {
    // alert('登录失败')
    // const errorMessage = error.response?.data?.message || '登录失败，请重试'
    alert(error.message)
  }
}
</script>