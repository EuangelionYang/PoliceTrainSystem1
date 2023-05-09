import request from '@/utils/request'

// 获取训练所有分类信息
export function getCatagoryList(data) {
  return request({
    url: '/api/training/category/',
    method: 'get',
    params: data
  })
}
'/api/training/category/?no_page=1&type=情绪课程分类'
// 获取一个分类的信息
export function getCatagory(id) {
  return request({
    url: '/api/training/category/' + id + '/',
    method: 'get'
  })
}

// 训练添加分类
export function addCatagory(data) {
  return request({
    url: '/api/training/category/',
    method: 'post',
    data: data
  })
}

// 训练修改分类
export function updateCatagory(id, data) {
  return request({
    url: '/api/training/category/' + id + '/',
    method: 'put',
    data: data
  })
}

// 训练删除分类
export function deleteOneCatagory(id) {
  return request({
    url: '/api/training/category/' + id + '/',
    method: 'delete'
  })
}

// 训练删除分类_多选
export function deleteCatagory(data) {
  return request({
    url: '/api/training/category/multiple_delete/',
    method: 'delete',
    data: data
  })
}
