import Cookies from 'js-cookie'
// 该js文件为操作token的基础模板
const TokenKey = 'access'
// 提供了获取token、设置token、删除token的方法，可以直接使用
export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
