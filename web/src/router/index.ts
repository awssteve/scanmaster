import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/scan',
    name: 'Scan',
    component: () => import('@/views/Scan.vue')
  },
  {
    path: '/id-card',
    name: 'IDCard',
    component: () => import('@/views/IDCard.vue')
  },
  {
    path: '/documents',
    name: 'Documents',
    component: () => import('@/views/Documents.vue')
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue')
  },
  {
    path: '/result/:id',
    name: 'Result',
    component: () => import('@/views/Result.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/batch',
    name: 'Batch',
    component: () => import('@/views/Batch.vue')
  },
  {
    path: '/advanced',
    name: 'Advanced',
    component: () => import('@/views/Advanced.vue')
  },
  {
    path: '/advanced/watermark',
    name: 'Watermark',
    component: () => import('@/views/Watermark.vue')
  },
  {
    path: '/advanced/translate',
    name: 'Translate',
    component: () => import('@/views/Translate.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
