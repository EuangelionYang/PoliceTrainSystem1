import request from '@/utils/request'

// 获取动作列表
export function getActionList(query) {
  return request({
    url: '/api/training/action/',
    method: 'get',
    params: query
  })
}
// 获取动作列表
export function getAction(id) {
  return request({
    url: '/api/training/action/' + id + '/',
    method: 'get'
  })
}

// 新增动作
export function addAction(data) {
  return request({
    url: '/api/training/action/',
    method: 'post',
    data: data
  })
}

// 修改动作
export function updateAction(id, data) {
  return request({
    url: '/api/training/action/' + id + '/',
    method: 'put',
    data: data
  })
}

// 删除动作
export function deleteOneAction(id) {
  return request({
    url: '/api/training/action/' + id + '/',
    method: 'delete'
  })
}

// 删除动作_多选
export function deleteAction(data) {
  return request({
    url: '/api/training/action/multiple_delete/',
    method: 'delete',
    data: data
  })
}
