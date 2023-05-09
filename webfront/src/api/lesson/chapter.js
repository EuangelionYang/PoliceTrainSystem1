import request from '@/utils/request'

// 获取训练所有章节信息
export function getChapterList(data) {
  return request({
    url: '/api/training/training/get_chaptersByTrainingID/',
    method: 'post',
    data: data
  })
}

// 获取一个章节的信息
export function getChapter(id) {
  return request({
    url: '/api/training/chapter/' + id + '/',
    method: 'get'
  })
}

// 训练添加章节
export function addChapter(data) {
  return request({
    url: '/api/training/chapter/',
    method: 'post',
    data: data,
    timeout: 5000000
  })
}

// 训练修改章节
export function updateChapter(id, data) {
  return request({
    url: '/api/training/chapter/' + id + '/',
    method: 'put',
    data: data
  })
}

// 训练删除章节
export function deleteChapter(id) {
  return request({
    url: '/api/training/chapter/' + id + '/',
    method: 'delete'
  })
}

// 根据章节id获取训练点
// data = { chapter_id: xxx }
export function getChapterPoints(data) {
  return request({
    url: '/api/training/chapter/get_pointsByChapterID/',
    method: 'post',
    data: data
  })
}

export function generateChapterKeyframe(data) {
  return request({
    url: '/api/training/keyframe/create_keyframe/',
    method: 'post',
    data: data
  })
}

export function getChapterKeyframe(data) {
  return request({
    url: '/api/training/chapter/get_keyframeByChapterID/',
    method: 'post',
    data: data
  })
}

export function editChapterKeyframe(id, data) {
  return request({
    url: '/api/training/keyframe/' + id + '/',
    method: 'put',
    data: data
  })
}

// 增加训练点
export function addChapterPoints(data) {
  return request({
    url: '/api/training/training_point/',
    method: 'post',
    data: data
  })
}

// 删除训练点
export function deleteChapterPoints(id) {
  return request({
    url: '/api/training/training_point/' + id + '/',
    method: 'delete'
  })
}

