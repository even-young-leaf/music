import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

// 路由懒加载
const Index = () => import('../views/Index.vue')
const Ranking = () => import('../views/Ranking.vue')
const Play = () => import('../views/Play.vue')
const Search = () => import('../views/Search.vue')
const User = () => import('../views/User.vue')

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index
  },
  {
    path: '/ranking',
    name: 'Ranking',
    component: Ranking
  },
  {
    path: '/play/:id',
    name: 'Play',
    component: Play
  },
  {
    path: '/search/:page',
    name: 'Search',
    component: Search
  },
  {
    path: '/user/:id',
    name: 'User',
    component: User
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router