import request from '@/utils/request'

// 获取部门列表
export function getDeptList() {
  return request({
    url: '/api/rbac/dept/get_dept_tree/',
    method: 'get'
  })
}

// 获取部门列表
export function getDeptOne(id) {
  return request({
    url: '/api/rbac/dept/' + id + '/',
    method: 'get'
  })
}

// 新增部门
export function addDept(data) {
  return request({
    url: '/api/rbac/dept/',
    method: 'post',
    data: data
  })
}

// 修改部门
export function updateDept(id, data) {
  return request({
    url: '/api/rbac/dept/' + id + '/',
    method: 'put',
    data: data
  })
}

// 删除部门
export function deleteDept(id) {
  return request({
    url: '/api/rbac/dept/' + id,
    method: 'delete'
  })
}
