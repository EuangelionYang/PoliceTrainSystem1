import request from '@/utils/request'

// 获取角色列表
export function getRoleList(data) {
  return request({
    url: '/api/rbac/role/',
    method: 'get',
    params: data
  })
}

// 查询用户列表
export function listUser(data) {
  return request({
    url: '/api/rbac/user/',
    method: 'get',
    params: data
  })
}

// 查询单个用户信息
export function getUniqueUser(id) {
  return request({
    url: '/api/rbac/user/' + id,
    method: 'get'
  })
}

// 添加用户
export function addUser(data) {
  return request({
    url: '/api/rbac/user/',
    method: 'post',
    data: data
  })
}

// 删除用户
export function deleteUser(data) {
  return request({
    url: '/api/rbac/user/multiple_delete/',
    method: 'delete',
    data: data
  })
}

// 修改用户
export function updateUser(id, data) {
  return request({
    url: '/api/rbac/user/' + id + '/',
    method: 'put',
    data: data
  })
}

// 修改用户部分信息
export function updateUserPartial(id, data) {
  return request({
    url: '/api/rbac/user/' + id + '/',
    method: 'patch',
    data: data
  })
}

// 重置密码
export function resetPassword(data) {
  return request({
    url: '/api/reset_password/',
    method: 'post',
    data: data
  })
}

// 修改密码
export function updatePassword(data) {
  return request({
    url: '/api/update_password/',
    method: 'post',
    data: data
  })
}

// 获取用户人脸数据
export function getUserFace(data) {
  return request({
    url: '/api/rbac/user_face/get_facesByID/',
    method: 'post',
    data: data
  })
}

// 增加用户人脸数据
// data:{ uid, face[file]}
export function addUserFace(data) {
  return request({
    url: '/api/rbac/user_face/',
    method: 'post',
    data: data
  })
}

// 删除用户人脸数据
// id: picId
export function deleteUserFace(id) {
  return request({
    url: '/api/rbac/user_face/' + id + '/',
    method: 'delete'
  })
}

// 用户数据导出
export function userExport(data) {
  return request({
    url: '/api/rbac/user/export/',
    method: 'post',
    data: data
  })
}

// 用户数据导入
export function userImport(data) {
  return request({
    url: '/api/rbac/user/import/',
    method: 'post',
    data: data
  })
}

