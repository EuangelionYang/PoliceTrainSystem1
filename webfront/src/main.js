import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css
import VideoPlayer from 'vue-video-player' // 导入视频播放插件
import TreeTable from 'vue-table-with-tree-grid'
import vuescroll from 'vuescroll' // 导入滚动条插件
import * as echarts from 'echarts'
import 'vuescroll/dist/vuescroll.css'
require('vue-video-player/src/custom-theme.css')
require('video.js/dist/video-js.css')
import App from './App'
import store from './store'
import router from './router'
import axios from 'axios'
import vuex from 'vuex'
import tracking from 'tracking'
import '@/icons' // icon
import '@/permission' // permission control
import global from '@/utils/common'
// import FileSaver from 'file-saver'
import XLSX from 'xlsx'
import SvgIcon from './components/SvgIcon/index'
import uploader from 'vue-simple-uploader'
Vue.component('svg-icon', SvgIcon) // 注册全局组件
const req = require.context('./icons/svg', false, /\.svg$/)
const requireAll = requireContext => requireContext.keys().map(requireContext)
requireAll(req)
// set ElementUI lang to EN
Vue.use(ElementUI)
Vue.use(VideoPlayer)
Vue.use(vuescroll)
Vue.use(vuex)
Vue.use(tracking)
Vue.use(XLSX)
Vue.use(uploader)

Vue.component('tree-table', TreeTable)
// 如果想要中文版 element-ui，按如下方式声明
// Vue.use(ElementUI)
Vue.prototype.$axios = axios
Vue.prototype.$echarts = echarts
Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
  // beforeCreate() {
  //   // 全局事件总线
  //   // A与B是兄弟，B要给A发送信息,A收到信息以后打印出来
  //   // A.$bus.$on('sendMessage',console.log(message))
  //   // B.$bus.$emit('sendMessage',message)
  //   Vue.prototype.$bus = this
  // }
}).$mount('#app')

// 这个方法是监测浏览器窗口发生变化的时候执行
window.addEventListener('visibilitychange', function() {
  if (document.hidden === false && global.aaa !== localStorage.getItem('loginToken')) {
    // 只有当初始创建的token不等于localStorage里面的token的时候去覆盖掉这个token的值并且需要先刷新浏览器窗口
    // 原生JS提供的方法
    window.location.reload()
    global.aaa = localStorage.getItem('loginToken')
  } else {
    global.aaa = localStorage.getItem('loginToken')
  }
  // 不覆盖的话username永远都是我们设的初始值
})
