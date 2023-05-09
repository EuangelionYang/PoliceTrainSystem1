// 整个路由逻辑在这个文件
import router from './router'
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { getToken } from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

// 免登录白名单
const whiteList = ['/login']
// 路由守卫,全局钩子,每一次页面刷新都会执行
router.beforeEach((to, from, next) => {
  // 开始加载
  NProgress.start()

  // 设置标题
  document.title = getPageTitle(to.meta.title)
  // 获取token
  const hasToken = getToken()
  // 这里就会先判断是否有token如果没有直接跳转到登录页面
  if (hasToken) {
    // 如果有token，根据to.path也就是你将要跳转到的页面路由如果是登录那就通过next（）放行
    if (to.path === '/login') {
      next({ path: '/login' })
      NProgress.done() // 加载完成
    } else {
      // else如果不是登录的路由，进去通过所有vuex中暴露出来的值也就是store\getters.js获取到user.js中的角色是否为空
      // 判断是否获取了用户信息并拿到roles
      const hasRoles = store.getters.roles && store.getters.roles.length > 0
      // 如果不为空,说明store\modules\permission.js这里面已经筛选过路由直接通过next()放行
      if (hasRoles) {
        // console.log('有用户信息')
        next() // 如果获取了 放行
      } else { // 没有就获取用户信息
        // else如果没有获取到角色，
        // 通过const { roles } = await store.dispatch(‘user/getInfo’)这个去store\modules\user.js获取角色信息，
        // 然后再调用 const accessRoutes = await store.dispatch(‘permission/generateRoutes’, roles)去文件store\modules\permission.js筛选出指定的路由返回
        // console.log('没有用户信息')
        try {
          // 返回的roles必须是object array,如: ['admin'] or ,['developer','editor']
          store.dispatch('user/getInfo').then(res => {
            const roles = res.roles
            store.dispatch('permission/getBtnPermission').then(() => {
              store.dispatch('permission/generateRoutes', { roles }).then(accessedRoutes => {
                router.addRoutes(accessedRoutes)
                accessedRoutes.forEach((item, index) => {
                  router.options.routes[index] = item
                })
                next({ ...to, replace: true })
              })
            })
          })
          // const { roles } = await store.dispatch('user/getInfo') // 通过token获取相应权限数组
          // const accessRoutes = await store.dispatch('permission/generateRoutes', roles)
          // router.addRoutes(accessRoutes) //  动态添加可访问路由，生成侧边栏
          // next({ ...to, replace: true })// 加载路由
          // hack方法，以确保addRoutes是完整的
          // 设置replace: true，这样导航将不会留下历史记录 record
          // 调用next({ …to, replace: true })让router.beforeEach（）重新执行一遍
        } catch (error) {
          // 删除token,进入登录页面重新登录
          store.dispatch('user/resetToken')
          Message.error(error || 'Has Error')
          next(`/login?redirect=${to.path}`)
          NProgress.done()
        }
      }
    }
  } else {
    // 没有token
    if (whiteList.indexOf(to.path) !== -1) {
      // 在白名单中的path 直接放行
      next()
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
