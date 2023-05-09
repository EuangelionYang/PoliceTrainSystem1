import { constantRoutes } from '@/router'
import { getRouters, getPermission } from '@/api/menu'
import Layout from '@/layout'
// import { mapGetters } from 'vuex'
// import store from "@/store";
// export function rFormat(routers) {
// // 简单检查是否是可以处理的数据
//   if (!(routers instanceof Array)) {
//     return false
//   }
//   // 处理后的容器
//   const fmRouters = []
//   routers.forEach(router => {
//     const path = router.path
//     const component = router.component
//     const name = router.name
//     const hidden = router.hidden
//     let children = router.children
//     const meta = router.meta
//     const redirect = router.redirect
//     // 如果有子组件，递归处理
//     if (children && children instanceof Array) {
//       children = rFormat(children)
//     }
//     const fmRouter = {
//       path: path,
//       // 拼出相对路径，由于component无法识别变量
//       // 利用Webpack 的 Code-Splitting 功能
//       component(resolve) {
//         let componentPath = ''
//         if (component === 'Layout') {
//         // Layout作为特殊组件处理，当然后端也可以写成'/layout/Layout.vue
//           require(['@/layout'], resolve)
//           return
//         } else {
//         // '@/views'要拼接进去，组件直接返回'@/views/xxxx/xxx.vue'，然后require([compoent],resolve)会报错
//         // require([`@/views/${component}`], resolve)
//           componentPath = component
//         }
//         require([`@/views/${componentPath}`], resolve)
//       },
//       name: name,
//       hidden: hidden,
//       children: children,
//       meta: meta,
//       redirect: redirect
//     }
//     fmRouters.push(fmRouter)
//   })
//   return fmRouters
// }

export function filterAsyncRouter(asyncRouterMap) {
  // 遍历后台传来的路由字符串，转换为组件对象
  const accessedRouters = asyncRouterMap.filter(route => {
    if (route.component) {
      if (route.component === 'Layout') {
        // Layout组件特殊处理
        route.component = Layout
      } else {
        route.component = loadView(route.component)
        // const component = route.component
        // route.component = resolve => require(['@/view' + component], resolve)
      }
    }
    if (route.children && route.children.length) {
      route.children = filterAsyncRouter(route.children)
    }
    return true
  })
  return accessedRouters
}

export const loadView = (view) => {
  // return require(`@/views${view}`) // 空页面
  // return require(`@/views${view}`).default  // 有效
  return resolve => require([`@/views${view}`], resolve) // 有效
}
// 定义state
const state = {
  routes: [],
  addRoutes: [],
  menuID: '',
  menuBtn: [],
  tempBtn: []
}
// 创建mutations用于更改state
// 通过routes[],addrouters[]两个数组将筛选好的路由以及结合静态路由全部保存起来
const mutations = {
  SET_ROUTES: (state, routes) => {
    // const roles = []
    state.addRoutes = routes
    // if (true) {
    //   constantRoutes.forEach(function (value, index, array) {
    //     if (value.path === '/') {
    //       // console.log('删除前', value.children)
    //       array[index].children.forEach(function (_value, _index, _array) {
    //         // console.log(_value)
    //         if (_value.path === '/userInfo') {
    //           // console.log(_value)
    //           _array.splice(_index, 1)
    //         }
    //       })
    //     }
    //     console.log('删除后', value.children)
    //   })
    // }
    state.routes = constantRoutes.concat(routes)
  },
  SET_MENUBTN: (state, menus) => {
    state.menuBtn = menus
  },
  SET_MENUID: (state, menuid) => {
    state.menuID = menuid
  },
  SET_TEMPBTN: (state, btnList) => {
    state.tempBtn = btnList
  }
}

const actions = {
  // 这里是获取 权限路由 参数roles即用户信息中返回的roles（根据传过来的角色去筛选动态路由数组）
  generateRoutes({ commit }, roles) {
    return new Promise(resolve => {
      // 先查询后台并返回左侧菜单数据并把数据添加到路由
      getRouters(roles).then(response => {
        // console.log('拿到后端返回的 路由json数据')
        // console.log(response)
        // console.log('转换成vue可用的路由')
        // const sidebarRoutes = rFormat(response)
        const sidebarRoutes = filterAsyncRouter(response)
        sidebarRoutes.push({ path: '*', redirect: '/404', hidden: true })
        // console.log(sidebarRoutes)
        console.log(1)
        commit('SET_ROUTES', sidebarRoutes)
        resolve(sidebarRoutes)
        // generaMenu(asyncRoutes, data)
      }).catch(error => {
        console.log(error)
      })
    })
  },
  // 获取所有页面的btn权限
  getBtnPermission({ commit }) {
    return new Promise(resolve => {
      getPermission().then(res => {
        commit('SET_MENUBTN', res.menu_list)
        resolve()
      }).catch(err => {
        console.log(err)
      })
    })
  },
  getPagePermission({ commit }, data) {
    return new Promise(resolve => {
      data.menu.forEach(ele => {
        ele.children.forEach(element => {
          if (element.id === data.menuid) {
            commit('SET_TEMPBTN', element.button_list)
          }
        })
      })
      resolve()
    })
  },
  changeMenuID({ commit }, menuid) {
    return new Promise(resolve => {
      commit('SET_MENUID', menuid)
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
