import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

// TODO: 404 / default route and view for it

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/ViewLogin.vue')
  },
  {
    path: '/user/reservations',
    name: 'user/reservations',
    component: () => import(/* webpackChunkName: "userreservations" */ '../views/user/ViewUserReservations.vue')
  },
  {
    path: '/user/logout',
    name: 'user/logout',
    component: () => import(/* webpackChunkName: "userlogout" */ '../views/user/ViewUserLogout.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
