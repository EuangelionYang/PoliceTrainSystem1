import request from '@/utils/request'

// 获取该用户的训练列表——学生
// data={'uid'=用户id}
export function getTrainingListByUser(params, data) {
  return request({
    url: '/api/training/training/get_trainingByUser/',
    method: 'post',
    data: data,
    params: params
  })
}

// 获取训练列表——教官
export function getTrainingListByTeacher(query) {
  return request({
    url: '/api/training/training/get_trainingByTeacher/',
    method: 'get',
    params: query
  })
}

// 获取训练列表——教务
export function getTrainingListByEducation(query) {
  return request({
    url: '/api/training/training/',
    method: 'get',
    params: query
  })
}

// 获取一个训练
export function getOneTraining(id) {
  return request({
    url: '/api/training/training/' + id + '/',
    method: 'get'
  })
}

// 新增训练
export function addTraining(data) {
  return request({
    url: '/api/training/training/',
    method: 'post',
    data: data
  })
}

// 设置训练学员
export function setTrainingLearners(data) {
  return request({
    url: '/api/training/training/set_learners/',
    method: 'post',
    data: data
  })
}

// 修改训练
export function updateTraining(id, data) {
  return request({
    url: '/api/training/training/' + id + '/',
    method: 'put',
    data: data
  })
}

// 删除训练
export function deleteTraining(data) {
  return request({
    url: '/api/training/training/multiple_delete/',
    method: 'delete',
    data: data
  })
}

// 获取所有学员
export function getLearners(query) {
  return request({
    url: '/api/training/training/get_learners/',
    method: 'get',
    query: query
  })
}

// 获取所有教官
export function getTeachers() {
  return request({
    url: '/api/training/training/get_teachers/',
    method: 'get'
  })
}

// 课程审核接口
// data: {training_id:训练id, is_pass:0(驳回)/1(通过)}
export function doReview(data) {
  return request({
    url: '/api/training/training/review/',
    method: 'post',
    data: data
  })
}

// 课程发布接口
// data: {training_id:训练id}
export function doPublish(data) {
  return request({
    url: '/api/training/training/publish/',
    method: 'post',
    data: data
  })
}
