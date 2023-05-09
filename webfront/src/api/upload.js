import request from '@/utils/request'

export function upload(data) {
  return request({
    url: '/api/training/upload/',
    method: 'post',
    data
  })
}
export function complete(data) {
  return request({
    url: '/api/training/complete/',
    method: 'post',
    data
  })
}
export function checkMD5(data) {
  return request({
    url: '/api/checkmd5/',
    method: 'post',
    data
  })
}
