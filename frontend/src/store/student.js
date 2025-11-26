import { defineStore } from 'pinia'
import studentApi from '@/api/student'

export const useStudentStore = defineStore('student', {
  state: () => ({
    user: null,
    dormitory: null,
    fees: null,
    maintenanceRequests: [],
    changeRequests: [],
    personal_info: null
  }),
  actions: {
    async login(credentials) {
      try{
        const response = await studentApi.login(credentials)
        // print('response.data:', response.data) 
        // this.user = response.data.user
        this.user = response.user
        // localStorage.setItem('token', response.data.token)
        // return response.data.message
        await this.fetchStudentInfo()
        return response.message
      } catch (error) {
        throw new Error(error.message)
      }
    },
    async logout() {
      await studentApi.logout()
      this.user = null
      // localStorage.removeItem('token')
    },
    async fetchDormitory() {
      try {
      const response = await studentApi.getDormitory()
      this.dormitory = response
    } catch (error) {
      throw new Error(error.message)
    }},
    async submitMaintenanceRequest(data) {
      try {
        const response = await studentApi.submitMaintenanceRequest(data)
        return response
      } catch (error) {
        throw new Error(error.message)
      }
    },
    async submitChangeRequest(data) {
      try {
        const response = await studentApi.submitChangeRequest(data)
        return response
      } catch (error) {
        throw new Error(error.message)
      }
    },
    async modifyMaintenanceRequest(data) {
      try {
        const response = await studentApi.modifyMaintenanceRequest(data)
        return response
      } catch (error) {
        throw new Error(error.message)
      }
    },
    async modifyChangeRequest(data) {
      try {
        const response = await studentApi.modifyChangeRequest(data)
        return response
      } catch (error) {
        throw new Error(error.message)
    }},
    async fetchFees() {
      try{
      const response = await studentApi.getFees()
      this.fees = response
      } catch (error) {
        throw new Error(error.message)
      }
    },
    async fetchMaintenanceRequests() {
      try{
      const response = await studentApi.getAllMaintenanceRequests()
      this.maintenanceRequests = response
      } catch (error) {
        throw new Error(error.message)
      }
    },
    async fetchChangeRequests() {
      try {
        const response = await studentApi.getAllChangeRequests()
        this.changeRequests = response // 
      } catch (error) {
        throw new Error(error.message)
      }
    },
    async fetchStudentInfo() {
      try {
        const response = await studentApi.getStudentInfo()
        this.personal_info = response
      } catch (error) {
        throw new Error(error.message)
      }
    },
    async modifyInfo(data) {
      try {
        const response = await studentApi.modifyInfo(data)
        this.personal_info = response
        return response.message
      } catch (error) {
        throw new Error(error.message)
      }
    }
  }
})