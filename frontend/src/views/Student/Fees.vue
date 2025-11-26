<template>
  <div>
    <router-link to="/student/dashboard" class="back-to-dashboard">← 返回仪表盘</router-link>
    <h2>宿舍费用概览</h2>

    <!-- 加载中提示 -->
    <div v-if="!studentStore.fees">
      <p>正在加载费用信息...</p>
    </div>

    <!-- 数据加载成功 -->
    <div v-else>
      <!-- 显示所有费用记录 -->
      <h3>费用明细</h3>
      <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
        <thead>
          <tr>
            <th>学年</th>
            <th>学期</th>
            <th>宿舍号</th>
            <th>应缴金额</th>
            <th>已缴金额</th>
            <th>剩余金额</th>
            <th>支付状态</th>
            <th>截止日期</th>
            <th>支付日期</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(fee, index) in studentStore.fees.data.fees" :key="index">
            <td>{{ fee.academic_year }}</td>
            <td>{{ fee.semester }}</td>
            <td>{{ fee.dormitory_no }}</td>
            <td>{{ fee.fee_amount }}</td>
            <td>{{ fee.paid_amount }}</td>
            <td>{{ fee.remaining_amount }}</td>
            <td>{{ fee.payment_status }}</td>
            <td>{{ fee.due_date }}</td>
            <td>{{ fee.payment_date }}</td>
          </tr>
        </tbody>
      </table>

      <!-- 可选：显示总金额 -->
      <h3>汇总</h3>
      <p>总应缴金额：{{ totalFeeAmount }}</p>
      <p>总已缴金额：{{ totalPaidAmount }}</p>
      <p>总剩余金额：{{ totalRemainingAmount }}</p>
    </div>

    <button @click="fetchFees">刷新</button>
  </div>
</template>

<script setup>
import { useStudentStore } from '@/store/student'
import { computed } from 'vue'

const studentStore = useStudentStore()

// 计算属性：计算总金额
const totalFeeAmount = computed(() => {
  if (!studentStore.fees?.data?.fees) return 0
  return studentStore.fees.data.fees.reduce((sum, fee) => sum + (fee.fee_amount || 0), 0)
})

const totalPaidAmount = computed(() => {
  if (!studentStore.fees?.data?.fees) return 0
  return studentStore.fees.data.fees.reduce((sum, fee) => sum + (fee.paid_amount || 0), 0)
})

const totalRemainingAmount = computed(() => {
  if (!studentStore.fees?.data?.fees) return 0
  return studentStore.fees.data.fees.reduce((sum, fee) => sum + (fee.remaining_amount || 0), 0)
})

const fetchFees = async () => {
  await studentStore.fetchFees()
}
</script>