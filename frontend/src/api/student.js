import axios from 'axios'

const API_BASE_URL = '/api/student'

// const apiClient = axios.create({
//   baseURL: API_BASE_URL,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// })

export default {
  // 注册
  register(data) {
    const formData = new FormData()
    formData.append('student_id', data.student_id)
    formData.append('password', data.password)
    formData.append('name', data.name)
    formData.append('major', data.major)
    formData.append('email', data.email)
    formData.append('gender', data.gender)
    formData.append('phone_number', data.phone_number)
    return axios.post(`${API_BASE_URL}/register`, formData)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 登录
  login(data) {
    const formData = new FormData()
    formData.append('student_id', data.student_id)
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
  getStudentInfo() {
    return axios.get(`${API_BASE_URL}/info`)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 修改个人信息
  modifyInfo(data) {
    const formData = new FormData()
    formData.append('name', data.name)
    formData.append('gender', data.gender)
    formData.append('major', data.major)
    formData.append('email', data.email)
    formData.append('phone_number', data.phone_number)
    return axios.post(`${API_BASE_URL}/modify`, formData)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 获取宿舍信息
  getDormitory() {
    return axios.get(`${API_BASE_URL}/dormitory`)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 提交宿舍更换请求
  submitChangeRequest(data) {
    const formData = new FormData()
    formData.append('new_dormitory_no', data.new_dormitory_no)
    formData.append('reason', data.reason)
    return axios.post(`${API_BASE_URL}/dormitory/change_request`, formData)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 获取费用概览
  getFees() {
    return axios.get(`${API_BASE_URL}/dormitory/fees`)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 提交维修请求
  submitMaintenanceRequest(data) {
    const formData = new FormData()
    formData.append('issue', data.issue)
    formData.append('priority', data.priority)
    return axios.post(`${API_BASE_URL}/maintenance/request`, formData)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 获取所有维修请求
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
  // 修改维修请求（需传 request_id）
  modifyMaintenanceRequest(data) {
    const formData = new FormData()
    formData.append('issue', data.issue)
    formData.append('priority', data.priority)
    formData.append('request_id', data.request_id)
    return axios.post(`${API_BASE_URL}/maintenance/modify_request`, formData)
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
    return axios.get(`${API_BASE_URL}/dormitory/all_change_requests`)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 修改宿舍更换请求（需传 request_id）
  modifyChangeRequest(data) {
    const formData = new FormData()
    formData.append('reason', data.reason)
    formData.append('new_dormitory_no', data.new_dormitory_no)
    formData.append('request_id', data.request_id)
    return axios.post(`${API_BASE_URL}/dormitory/modify_change_request`, formData)
      .then(response => {
        if (response.data.success) {
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      })
  },
  // 登出
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