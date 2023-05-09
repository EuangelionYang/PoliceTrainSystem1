import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/login/',
    method: 'post',
    data
  })
}
export function facelogin(data) {
  return request({
    url: '/api/faceid/',
    method: 'post',
    data
  })
}
export function getInfo() {
  return request({
    url: '/api/rbac/user/info/',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/api/logout/',
    method: 'get'
  })
}
