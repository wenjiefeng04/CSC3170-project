<template>
  <div class="container">
    <!-- 返回仪表盘按钮 -->
    <router-link to="/admin/dashboard" class="back-to-dashboard">← 返回仪表盘</router-link>

    <h2>宿舍状态管理</h2>

    <!-- 刷新按钮 -->
    <button @click="fetchDormitoryStatus" class="refresh-btn">🔄 刷新宿舍状态</button>

    <!-- 加载中提示 -->
    <div v-if="adminStore.loading" class="loading">
      <p>正在加载宿舍状态...</p>
    </div>

    <!-- 无数据提示 -->
    <div v-else-if="dormitoryStatusList.length === 0" class="no-data">
      <p>暂无宿舍数据</p>
    </div>

    <!-- 宿舍状态表格 -->
    <div v-else class="dormitory-table-container">
      <table class="dormitory-table">
        <thead>
          <tr>
            <th>宿舍号</th>
            <th>楼栋</th>
            <th>楼层</th>
            <th>门牌号</th>
            <th>总床位</th>
            <th>已占用</th>
            <th>空床位</th>
            <th>入住状态</th>
            <th>最新缴费状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dorm in dormitoryStatusList" :key="dorm.dormitory_no" class="dorm-row">
            <td>{{ dorm.dormitory_no }}</td>
            <td>{{ dorm.building_no }}</td>
            <td>{{ dorm.floor_no }}</td>
            <td>{{ dorm.dormitory_door_no }}</td>
            <td>{{ dorm.total_beds }}</td>
            <td>{{ dorm.occupied_beds }}</td>
            <td :class="dorm.available_beds > 0 ? 'available-beds' : 'no-available-beds'">
              {{ dorm.available_beds }}
            </td>
            <td :class="dorm.room_availability === '未满' ? 'status-available' : 'status-full'">
              {{ dorm.room_availability }}
            </td>
            <td :class="getPaymentStatusClass(dorm.latest_payment_status)">
              {{ dorm.latest_payment_status }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/store/admin'

const adminStore = useAdminStore()

// 消息状态
const message = ref(null)

// 计算属性：获取宿舍状态列表
const dormitoryStatusList = computed(() => {
  if (!adminStore.dormitoryStatus?.data?.dormitories) {
    return []
  }
  return adminStore.dormitoryStatus.data.dormitories
})

// 获取缴费状态的样式类
const getPaymentStatusClass = (status) => {
  switch (status) {
    case '已支付':
      return 'payment-paid'
    case '部分支付':
      return 'payment-partial'
    case '未支付':
      return 'payment-unpaid'
    default:
      return 'payment-unknown'
  }
}

// 刷新宿舍状态
const fetchDormitoryStatus = async () => {
  try {
    adminStore.loading = true
    await adminStore.fetchAllDormitoryStatus()
    message.value = null
  } catch (error) {
    message.value = {
      type: 'error',
      text: '加载宿舍状态失败：' + error.message
    }
    setTimeout(() => {
      message.value = null
    }, 3000)
  } finally {
    adminStore.loading = false
  }
}

// 页面加载时获取宿舍状态
onMounted(() => {
  fetchDormitoryStatus()
})
</script>

<style scoped>
.container {
  padding: 20px;
}

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

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.refresh-btn {
  margin-bottom: 20px;
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}

.refresh-btn:hover {
  background: #0056b3;
}

.loading, .no-data {
  text-align: center;
  padding: 40px 0;
  color: #666;
  font-size: 1.1em;
}

.dormitory-table-container {
  overflow-x: auto;
}

.dormitory-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dormitory-table th,
.dormitory-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.dormitory-table th {
  background: #f8f9fa;
  font-weight: bold;
  color: #495057;
}

.dorm-row:hover {
  background: #f8f9fa;
}

.available-beds {
  color: #28a745;
  font-weight: bold;
}

.no-available-beds {
  color: #dc3545;
}

.status-available {
  color: #28a745;
  font-weight: bold;
}

.status-full {
  color: #dc3545;
}

.payment-paid {
  color: #28a745;
  font-weight: bold;
}

.payment-partial {
  color: #ffc107;
  font-weight: bold;
}

.payment-unpaid {
  color: #dc3545;
  font-weight: bold;
}

.payment-unknown {
  color: #6c757d;
}
</style>