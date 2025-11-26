import { defineStore } from 'pinia'
import adminApi from '@/api/admin'
import admin from '../api/admin'
export const useAdminStore = defineStore('admin', {
  state: () => ({
    user: null,
    students: [],
    changeRequests: [],
    dormitoryStatus: [],
    maintenanceRequests: [],
    admin_info: null
  }),
  actions: {
    async login(credentials) {
      try{
      const response = await adminApi.login(credentials)
      this.user = response.name} catch (error) {
        throw new Error(error.message)
      }
      // localStorage.setItem('admin_token', response.data.token)
    },
    async logout() {
      try{
      await adminApi.logout()
      this.user = null} catch (error) {
        throw new Error(error.message)
      }
      // localStorage.removeItem('admin_token')
    },
    async fetchAllStudents() {
      const response = await adminApi.getAllStudents()
      this.students = response.data.students
    },
    async modifyStudentAccount(data) {
      const response = await adminApi.modifyStudentAccount(data)
      await this.fetchAllStudents()
      return response
    },
    async fetchAdminInfo() {
      const response = await adminApi.getAdminInfo()
      this.admin_info = response.data
    },
    async modifyOwnInfo(data) {
      try {
        const response = await adminApi.modifyOwnInfo(data)
        await this.fetchAdminInfo()
      } catch (error) {
        throw new Error(error.message) // 抛出错误，让组件捕获
      }
    },
    async fetchAllChangeRequests() {
      const response = await adminApi.getAllChangeRequests()
      this.changeRequests = response
    },
    async fetchAllDormitoryStatus() {
      const response = await adminApi.getAllDormitoryStatus()
      this.dormitoryStatus = response
    },
    async fetchAllMaintenanceRequests() {
      const response = await adminApi.getAllMaintenanceRequests()
      this.maintenanceRequests = response
    },
    async approveChangeRequest(data) {
      await adminApi.approveChangeRequest(data)
      await this.fetchAllChangeRequests()
    },
    async processMaintenanceRequest(data) {
      await adminApi.processMaintenanceRequest(data)
      await this.fetchAllMaintenanceRequests()
      // 可选：刷新维修请求列表
    }
  }
})