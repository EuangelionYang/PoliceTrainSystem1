import { login, logout, getInfo, facelogin } from '@/api/login'
import { getToken, setToken, removeToken } from '@/utils/auth'
import global from '@/utils/common'
// import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    // 设置token的共享状态，token持久化 => 放到缓存中
    token: getToken(),
    id: '',
    username: '',
    name: '',
    avatar: '',
    identifier: [],
    roles: []
  }
}
// 状态
const state = getDefaultState()
// 修改状态
const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_ID: (state, id) => {
    state.id = id
  },
  SET_USERNAME: (state, username) => {
    state.username = username
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_IDENTIFIER: (state, identifier) => {
    state.identifier = identifier
  }
}
// 执行异步
const actions = {
  // 封装axios进行异步请求，在顶部看到是src目录下的api文件夹中的user.js引入进来的login的api接口
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    // 发送网路请求,登录操作,调用api中user的login
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const data = response
        // 设置token,作为用户已经登录的前端标志,存在sessionstorage中
        // 2.更改store中的状态 通过提交mutations 调用commit方法，第一个参数 一个回调函数，执行修改逻辑的函数，第二个 是mutations的载荷(一般为你需要修改的状态值)
        commit('SET_TOKEN', data.access)
        commit('SET_ID', data.id)
        commit('SET_USERNAME', data.username)
        commit('SET_AVATAR', data.avatar)
        setToken(data.access)
        global.aaa = data.access
        window.localStorage.setItem('loginToken', data.access)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },
  facelogin({ commit }, imgUrl) {
    // 发送网路请求,登录操作,调用api中user的login
    return new Promise((resolve, reject) => {
      facelogin({ 'face_base64': imgUrl }).then(response => {
        const data = response
        commit('SET_TOKEN', data.access)
        commit('SET_ID', data.id)
        commit('SET_USERNAME', data.username)
        commit('SET_AVATAR', data.avatar)
        setToken(data.access)
        global.aaa = data.access
        window.localStorage.setItem('loginToken', data.access)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // ----这里已经拿到token,拿到token后,通过token获取用户信息
  // 3.获取用户的角色信息
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.id).then(response => {
        const user = response
        const { role_list } = user
        const { identifier_list } = user
        // roles must be a non-empty array
        if (!role_list || role_list.length <= 0) {
          reject('getInfo: roles must be a non-null array!')
        }
        commit('SET_NAME', user.name)
        commit('SET_ID', user.id)
        commit('SET_AVATAR', user.avatar)
        commit('SET_ROLES', role_list)
        commit('SET_IDENTIFIER', identifier_list)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout().then(() => {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        removeToken() // must remove  token  first
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
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

