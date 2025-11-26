import axios from 'axios'

const API_BASE_URL = '/api/admin'

export default {
  // 管理员登录
  login(data) {
    const formData = new FormData()
    formData.append('admin_id', data.admin_id)
    formData.append('password', data.password)
    return axios.post(`${API_BASE_URL}/login`, formData)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 获取所有学生账户
  getAllStudents() {
    return axios.get(`${API_BASE_URL}/students/all_accounts`)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  getAdminInfo() {
    return axios.get(`${API_BASE_URL}/admin_info`)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else { 
          throw new Error(response.data.message)
        }
      })
  },
  // 修改管理员个人信息
  modifyOwnInfo(data) {
    const formData = new FormData()
    // formData.append('admin_id', data.admin_id)
    formData.append('name', data.name)
    formData.append('email', data.email)
    formData.append('phone_number', data.phone_number)
    return axios.post(`${API_BASE_URL}/modify_account`, formData)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 修改学生账户信息
  modifyStudentAccount(data) {
    const formData = new FormData()
    formData.append('student_id', data.student_id)
    formData.append('name', data.name)
    formData.append('gender', data.gender)
    formData.append('major', data.major)
    formData.append('email', data.email)
    formData.append('phone_number', data.phone_number)
    return axios.post(`${API_BASE_URL}/student/modify_account`, formData)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 获取所有宿舍更换请求
  getAllChangeRequests() {
    //const formData = new FormData()
    // formData.append('student_id', data.student_id)
    return axios.get(`${API_BASE_URL}/all_change_requests`)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 审批宿舍更换请求（批准/拒绝）
  approveChangeRequest(data) {
    const formData = new FormData()
    formData.append('student_id', data.student_id)
    formData.append('request_id', data.request_id)
    formData.append('action', data.action)
    return axios.post(`${API_BASE_URL}/student/approve_change_requests`, formData)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 获取所有宿舍状态
  getAllDormitoryStatus() {
    return axios.get(`${API_BASE_URL}/dormitory/all_status`)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  getAllMaintenanceRequests() {
    return axios.get(`${API_BASE_URL}/maintenance/all_requests`)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 处理维修请求（更新状态）
  processMaintenanceRequest(data) {
    const formData = new FormData()
    formData.append('request_id', data.request_id)
    formData.append('action', data.action)
    return axios.post(`${API_BASE_URL}/maintenance/process_request`, formData)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 管理员登出
  logout() {
    return axios.post(`${API_BASE_URL}/logout`)
    .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  }
}