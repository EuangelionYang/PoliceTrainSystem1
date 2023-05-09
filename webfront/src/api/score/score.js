import request from '@/utils/request'

// 查询某个训练全体学员的学习成绩
export function getLearnersGrade(query) {
  return request({
    url: '/api/training/training/get_learners_grade/',
    method: 'get',
    params: query
  })
}

// 查询单个学员的成绩接口
export function getOneLearnerGrade(query) {
  return request({
    url: '/api/training/training/my_grade/',
    method: 'get',
    params: query
  })
}

