import Vue from 'vue'
import App from './App.vue'
import router from '@/router/index.js'
import store from '@/store/index.js'
// import iView from 'iview'
import ViewUI from 'view-design';
import 'js/tool.js';
// 引入iview的css样式
import 'view-design/dist/styles/iview.css';

Vue.use(ViewUI)
Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
