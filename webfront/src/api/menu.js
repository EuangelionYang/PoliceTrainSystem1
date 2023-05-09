import request from '@/utils/request'

// 获取路由
export function getRouters() {
  return request({
    url: 'api/rbac/user/get_menus/',
    method: 'get'
  })
}

// 获取按钮权限
export function getPermission() {
  return request({
    url: '/api/rbac/menu/get_Menu_Button/',
    method: 'get'
  })
}
