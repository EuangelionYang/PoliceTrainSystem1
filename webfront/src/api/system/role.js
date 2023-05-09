import request from '@/utils/request'

// 查询角色列表
export function listRole(query) {
  return request({
    url: '/api/rbac/role/',
    method: 'get',
    params: query
  })
}

// 查询角色详细
export function getRole(id) {
  return request({
    url: '/api/rbac/role/' + id + '/',
    method: 'get'
  })
}

// 获取权限列表
export function getPermissionTree() {
  return request({
    url: '/api/rbac/menu/get_Menu_Button/',
    method: 'get'
  })
}

// 新增角色
export function addRole(data) {
  return request({
    url: '/api/rbac/role/',
    method: 'post',
    data: data
  })
}

// 修改角色
export function updateRole(id, data) {
  return request({
    url: '/api/rbac/role/' + id + '/',
    method: 'put',
    data: data
  })
}

// 角色状态修改
export function changeRoleStatus(id, data) {
  return request({
    url: '/api/rbac/role/' + id + '/',
    method: 'patch',
    data: data
  })
}

// 删除角色
export function deleteRoleOne(roleId) {
  return request({
    url: '/api/rbac/role/' + roleId + '/',
    method: 'delete'
  })
}

// 删除角色
export function deleteRole(data) {
  return request({
    url: '/api/rbac/role/multiple_delete/',
    method: 'delete',
    data: data
  })
}
