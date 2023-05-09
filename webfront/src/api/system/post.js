import request from '@/utils/request'

// 获取岗位列表
export function getPostList(query) {
  return request({
    url: '/api/rbac/post/',
    method: 'get',
    params: query
  })
}

// 获取岗位信息
export function getOnePost(id) {
  return request({
    url: '/api/rbac/post/' + id + '/',
    method: 'get'
  })
}

// 新增岗位
export function addPost(data) {
  return request({
    url: '/api/rbac/post/',
    method: 'post',
    data: data
  })
}

// 修改岗位
export function updatePost(id, data) {
  return request({
    url: '/api/rbac/post/' + id + '/',
    method: 'put',
    data: data
  })
}

// 删除岗位
export function deletePostOne(id) {
  return request({
    url: '/api/rbac/post/' + id + '/',
    method: 'delete'
  })
}

// 删除用户
export function deletePost(data) {
  return request({
    url: '/api/rbac/post/multiple_delete/',
    method: 'delete',
    data: data
  })
}
