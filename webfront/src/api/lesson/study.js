import request from '@/utils/request'

// 获取课程
export function getLessons(query) {
  return request({
    url: '/api/training/training/',
    method: 'get',
    params: query
  })
}

// 获取章节成绩
// post参数：training_id（课程主键），learner_id（学员主键）
export function getChapterGrade(data) {
  return request({
    url: '/api/training/training/get_chapter_grade/',
    method: 'post',
    data: data
  })
}

// 获取历史成绩
// post参数：training_id（课程主键），learner_id（学员主键）
export function getChapterHistoryGrade(data) {
  return request({
    url: '/api/training/training/get_chapter_history_grade/',
    method: 'post',
    data: data
  })
}

// 提交章节承接
// post参数：chapter_id（章节主键），learner_id（学员主键），grade（成绩）
export function submitChapterGrade(data) {
  return request({
    url: '/api/training/training/submit_chapter_grade/',
    method: 'post',
    data: data
  })
}
