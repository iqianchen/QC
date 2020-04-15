import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import http from '@/static/js/http.js'
import global from '@/static/js/global.js'

Vue.config.productionTip = false;
Vue.prototype.$http = http
Vue.prototype.$global = global

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
