import Vue from 'vue'
import Router from 'vue-router'
// 引入页面路径
import home from 'v/Home.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: home
    }
  ]
})