import Vue from "vue";
import Router from "vue-router";
import Home from 'p/home.vue'
import NoticeDetail from 'p/tabBarItems/noticeDetail'
import TestDetail from 'p/tabBarItems/testDetail'
import './cube-ui.js'

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      redirect: '/home'
    },{
      path: "/home",
      name: "home",
      component: Home
    },{
      path: '/notice/detail/:id',
      name: 'noticeDetail',
      component: NoticeDetail
    },{
      path: '/test/testDetail',
      name: 'noticeDetail',
      component: TestDetail
    }
  ]
});
