import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// axios拦截器:发送请求的基本路径配置
const service = axios.create({
  baseURL: process.env.BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 500000 // 超时时间
})

// 请求拦截器:主要处理token的"统一注入问题"
service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // 修改默认token名字,改为后端返回的token名字!!!未修改
      config.headers['Authorization'] = 'Bearer ' + getToken()
    }
    return config
  },
  error => {
    // do somet    // console.log(error     console.log(error) // for debug
    return Promise.reject(error)
  }
)

// 响应拦截器:主要处理返回的"数据异常"和"数据结构"问题
service.interceptors.response.use(res => {
  // 未设置状态码则默认成功状态
  const code = res.data.code || 200
  // 获取错误信息
  const msg = res.data.msg
  if (code === 401) {
    MessageBox.confirm('登录状态已过期，您可以继续留在该页面，或者重新登录', '系统提示', {
      confirmButtonText: '重新登录',
      cancelButtonText: '取消',
      type: 'warning'
    }
    ).then(() => {
      location.href = '/login'
    })
  } else if (code === 400) {
    Message({
      message: msg,
      type: 'error'
    })
    return Promise.reject(new Error(msg))
  } else {
    return res.data.data
  }
},
error => {
  // console.log('err' + error)
  let { message } = error
  // eslint-disable-next-line eqeqeq
  if (message == 'Network Error') {
    message = '后端接口连接异常'
  } else if (message.includes('timeout')) {
    message = '系统接口请求超时'
  } else if (message.includes('Request failed with status code')) {
    message = '系统接口' + message.substr(message.length - 3) + '异常'
  }
  Message({
    message: message,
    type: 'error',
    duration: 5 * 1000
  })
  return Promise.reject(error)
}
)

// 导出axios实例
export default service
