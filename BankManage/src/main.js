// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import VCharts from 'v-charts'
import VueRouter from 'vue-router'
import VueElementExtends from 'vue-element-extends'
import 'vue-element-extends/lib/index.css'
import VueResource from 'vue-resource'

Vue.config.productionTip = true

Vue.use(VueElementExtends)
Vue.use(VueRouter)
Vue.use(VueResource)
Vue.use(VCharts)
Vue.use(ElementUI)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
