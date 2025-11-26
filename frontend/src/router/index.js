import { createRouter, createWebHistory } from 'vue-router'
import LoginEntry from '../views/Auth/LoginEntry.vue'
import StudentLogin from '../views/Auth/StudentLogin.vue'
import StudentRegister from '../views/Auth/StudentRegister.vue'
import StudentDashboard from '../views/Student/Dashboard.vue'
import Dormitory from '../views/Student/Dormitory.vue'
import Fees from '../views/Student/Fees.vue'
import Maintenance from '../views/Student/Maintenance.vue'
import ChangeRequest from '../views/Student/ChangeRequest.vue'
import ModifyInfo from '../views/Student/ModifyInfo.vue'

const routes = [
  { path: '/', component: LoginEntry },
  { path: '/student/login', component: StudentLogin },
  { path: '/student/register', component: StudentRegister },
  { path: '/student/dashboard', component: StudentDashboard}, // , meta: { requiresAuth: true } },
  { path: '/student/dormitory', component: Dormitory}, //, meta: { requiresAuth: true } },
  { path: '/student/fees', component: Fees},//, meta: { requiresAuth: true } },
  { path: '/student/maintenance', component: Maintenance},//, meta: { requiresAuth: true } },
  { path: '/student/change-request', component: ChangeRequest},//, meta: { requiresAuth: true } },
  { path: '/student/modify-info', component: ModifyInfo},//, meta: { requiresAuth: true } },
  // 后续可添加管理员路由
  { path: '/admin/login', component: () => import('../views/Auth/AdminLogin.vue') },
  { path: '/admin/dashboard', component: () => import('../views/Admin/Dashboard.vue')},// meta: {  requiresAuth: true, role: 'admin' } },
  { path: '/admin/students', component: () => import('../views/Admin/Students.vue')},//, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/change-requests', component: () => import('../views/Admin/ChangeRequests.vue')},// meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/dormitory-status', component: () => import('../views/Admin/DormitoryStatus.vue')},//meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/maintenance', component: () => import('../views/Admin/Maintenance.vue')}//, meta: { requiresAuth: true, role: 'admin' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
// router.beforeEach((to, from, next) => {
//   const isAuthenticated = localStorage.getItem('token') || localStorage.getItem('admin_token')
//   const isAdmin = !!localStorage.getItem('admin_token')
//   const isStudent = !!localStorage.getItem('token')

//   if (to.meta.requiresAuth) {
//     if (!is) {
//       next('/student/login')
//     } else if (to.meta.role === 'admin' && !isAdmin) {
//       next('/student/dashboard') // 或者跳转到错误页
//     } else if (to.meta.role === 'student' && !isStudent) {
//       next('/admin/dashboard') // 或者跳转到错误页
//     } else {
//       next()
//     }
//   } else {
//     next()
//   }
// })

export default router