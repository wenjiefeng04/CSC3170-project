<template>
  <div>
    <router-link to="/student/dashboard" class="back-to-dashboard">← 返回仪表盘</router-link>
    <h2>宿舍信息</h2>

    <!-- 数据加载中提示（可选） -->
    <div v-if="!studentStore.dormitory">
      <p>正在加载宿舍信息...</p>
    </div>

    <!-- 数据加载成功 -->
    <div v-else>
      <!-- 我的宿舍 -->
      <h3>我的宿舍</h3>
      <p>楼号：{{ studentStore.dormitory.data.own_info.building_no }}</p>
      <p>楼层：{{ studentStore.dormitory.data.own_info.floor_no }}</p>
      <p>门牌号：{{ studentStore.dormitory.data.own_info.dormitory_door_no }}</p>
      <p>我的姓名：{{ studentStore.dormitory.data.own_info.student_name }}</p>

      <!-- 我的室友 -->
      <h3>我的室友</h3>
      <ul v-if="studentStore.dormitory?.data?.roommates?.length">
        <li v-for="(roommate, index) in studentStore.dormitory.data.roommates" :key="index">
          {{ roommate.roommate_name }}（{{ roommate.building_no }}-{{ roommate.floor_no }}-{{ roommate.dormitory_door_no }}）
        </li>
      </ul>
      <p v-else>暂无室友</p>
    </div>

    <button @click="fetchDormitory">刷新</button>
  </div>
</template>

<script setup>
import { useStudentStore } from '@/store/student'

const studentStore = useStudentStore()

const fetchDormitory = async () => {
  await studentStore.fetchDormitory()
}
</script>