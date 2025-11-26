<template>
  <div>
    <h2>管理员登录</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="form.admin_id" placeholder="管理员ID" required />
      <input v-model="form.password" type="password" placeholder="密码" required />
      <button type="submit">登录</button>
    </form>
    <p><router-link to="/">返回首页</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import adminApi from '@/api/admin'
import { useAdminStore } from '@/store/admin'

const router = useRouter()
const adminStore = useAdminStore()

const form = ref({
  admin_id: '',
  password: ''
})

const handleLogin = async () => {
  try {
    await adminStore.login(form.value)
    router.push('/admin/dashboard')
  } catch (error) {
    // alert('登录失败')
    // const errorMessage = error.response?.data?.message || '登录失败，请重试'
    alert(error.message)
  }
}
</script>