<template>
  <div id="userLayout" :style="{backgroundImage: 'url('+ imgBack +')'}">
    <div class="login_panle">
      <div class="login_panle_form">
        <div class="login_panle_form_title">
          <p class="login_panle_form_title_p">{{ appName }}</p>
        </div>
        <!-- 登录表单区域-->
        <el-form ref="loginForm" :model="loginForm" :rules="loginRules" auto-complete="on" label-position="left">
          <!-- 用户名 -->
          <el-form-item prop="username">
            <el-input
              ref="username"
              v-model="loginForm.username"
              placeholder="账号"
              name="username"
              type="text"
              tabindex="1"
              auto-complete="on"
            ><svg-icon slot="prefix" icon-class="user"/>
            </el-input>
          </el-form-item>
          <!-- 密码 -->
          <el-form-item prop="password">
            <el-input
              ref="password"
              :key="passwordType"
              v-model="loginForm.password"
              :type="passwordType"
              placeholder="密码"
              name="password"
              tabindex="2"
              auto-complete="on"
              @keyup.enter.native="handleLogin"
            ><svg-icon slot="prefix" icon-class="password" />
              <svg-icon slot="suffix" :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" @click="showPwd"/>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              :loading="loading"
              type="primary"
              style="width:45%"
              @click.native.prevent="handleLogin">登录
            </el-button>
            <el-button type="primary" style="width: 45%;margin-left:8%" @click.native.prevent="handleFace">刷脸登录
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      <div :style="{backgroundImage: 'url('+ imgLeft +')'}" class="login_panle_right"/>
      <div class="login_panle_foot">
        <!--  底部  -->
        <div class="el-login-footer">
          <span>Copyright © 2020-2021  All Rights Reserved.</span>
        </div>
      </div>
    </div>
    <!-- 人脸认证识别区域-->
    <el-dialog v-if="dialogFace" :visible.sync="dialogFace" title="刷脸登录" width="400px" @close="closeDialog">
      <!--      <el-button @click="playVideo" size="small" icon="el-icon-video-camera">打开摄像头</el-button>-->
      <div class="camera-wrapper">
        <!--        video标签用来显示摄像头内容 -->
        <video id="video" ref="refVideo" width="250" height="250" preload autoplay loop muted/>
        <!--       canvas用来画框框 -->
        <canvas id="canvas" ref="refCanvas" width="250" height="250"/>
        <span class="scanTip">{{ scanTip }}</span>
      </div>
    </el-dialog>
  </div>
</template>

<script>
/*eslint-disable */
import 'tracking/build/tracking'
import 'tracking/build/data/face'
import ImgBack from '@/assets/images/login_background.svg'
import ImgLeft from '@/assets/images/login_left.svg'
require('tracking/build/tracking-min')
require('tracking/build/data/face-min') // 脸部追踪
require('tracking/build/data/mouth-min') // 嘴部追踪
require('tracking/build/data/eye-min') // 眼部追踪
export default {
  name: 'Login',
  data() {
    return {
      appName: '执法训练成绩评估综合管理平台',
      imgBack: ImgBack,
      imgLeft: ImgLeft,
      dialogFace: false, // 弹窗
      loginForm: {
        username: '',
        password: ''
      },
      // 表单的验证规则对象
      loginRules: {
        // 验证用户名是否合法
        // required 是否为必填项
        // message 当前规则校验失败时的提示
        // trigger 表单验证的触发实际，blur表示失去焦点时触发
        username: [{ required: true, trigger: 'blur', message: '用户名不能为空' }],
        password: [{ required: true, trigger: 'blur', message: '密码不能为空' }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      tracker: null, // 人脸追踪器
      tipFlag: false, // 判断是否检测到
      flag: false, // 判断是否已经拍照
      removePhotoID: null, // 停止转换图片
      scanTip: '请保持人脸在采集框内', // 提示文字
      imgUrl: '', // base64格式图片
      canvas: null, // 页面画布元素
      video: null, // 页面视频元素
      context: null, // 画布内容
      streamIns: null // 视频流
    }
  },
  // watch route来监听路由变化
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    // 登录函数
    handleLogin() {
      // 登录校验
      this.$refs.loginForm.validate(valid => {
        // 如果校验通过
        if (valid) {
          this.loading = true
          // 如果通过表单校验规则就会进入user/login：是Vuex的状态管理模式方式调用，转到store的user.js里的login方法
          // dispatch（转发）的目的：
          // 1.发送login请求获取到token的值
          // 2.并存储到Vuex状态（类似全局的一个变量，能被子组件识别到）管理模式中，供多个组件同时识别使用
          this.$store.dispatch('user/login', this.loginForm).then(res => {
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 人脸认证开始
    handleFace() {
      this.dialogFace = true
      this.$nextTick(() => {
        this.playVideo()
      //   // this.canvas = document.getElementById('canvas')
      //   // this.context = this.canvas.getContext('2d')
      })
    },
    // 访问用户媒体设备
    getUserMedia(constrains, success, error) {
      // 使用navigator.mediaDevices.getUserMedia调用系统原生摄像头功能
      if (navigator.mediaDevices.getUserMedia) {
        // 最新标准API
        navigator.mediaDevices.getUserMedia(constrains).then(success).catch(error)
      } else if (navigator.webkitGetUserMedia) {
        // webkit内核浏览器
        navigator.webkitGetUserMedia(constrains).then(success).catch(error)
      } else if (navigator.mozGetUserMedia) {
        // Firefox浏览器
        navigator.mozGetUserMedia(constrains).then(success).catch(error)
      } else if (navigator.getUserMedia) {
        // 旧版API
        navigator.getUserMedia(constrains).then(success).catch(error)
      } else {
        this.scanTip = '你的浏览器不支持访问用户媒体设备'
      }
    },
    success(stream) {
      this.streamIns = stream
      // webkit内核浏览器
      this.URL = window.URL || window.webkitURL
      if ('srcObject' in this.$refs.refVideo) {
        // 视频播放
        this.$refs.refVideo.srcObject = stream
      } else {
        this.$refs.refVideo.src = this.URL.createObjectURL(stream)
      }
      this.$refs.refVideo.onloadedmetadata = e => {
        this.$refs.refVideo.play()
      }
    },
    error(e) {
      // this.scanTip = '访问用户媒体失败' + e.name + ',' + e.message
      this.$message({ showClose: true, message: '无法访问摄像头，请重新登录', type: 'warning' })
    },
    playVideo() {
      // 拿到媒体流
      this.getUserMedia({
        video: {
          width: 250, height: 250, facingMode: 'user'
        }/* 前置优先 */
      }, this.success, this.error)
      this.video = document.getElementById('video')
      this.canvas = document.getElementById('canvas')
      this.context = this.canvas.getContext('2d')
      // 使用监听人脸的包
      this.tracker = new tracking.ObjectTracker('face')
      this.tracker.setInitialScale(4)
      this.tracker.setStepSize(2)
      this.tracker.setEdgesDensity(0.1)
      // 每次打开弹框先清除canvas没拍的照片
      // this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)
      // 打开摄像头
      // 如果是读取视频，可以用trackerTask.stop trackerTask.run来暂停、开始视频
      tracking.track('#video', this.tracker, { camera: true })
      // 创建监听，每帧都会触发
      this.tracker.on('track', this.handleTracked)
    },
    //  tipFlag: false, // 是否检测
    // flag: false, // 判断是否已经拍照
    // 检测视频中人脸
    handleTracked(event) {
      if (!this.tipFlag) {
        if (event.data.length === 0) {
          // 未检测到人脸
          if (!this.flag) {
            this.scanTip = '未识别到人脸,请置于中央位置'
          }
        } else if (event.data.length === 1) {
          this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)
          // 检测到一张人脸
          if (!this.tipFlag) {
            this.scanTip = '识别成功，正在拍照，请勿乱动~'
            event.data.forEach(this.plot)
            if (!this.flag) {
              this.flag = true
              this.removePhotoID = setTimeout(() => {
                this.tackPhoto()
                this.tipFlag = true
              }, 2000)
            }
          }
        } else {
          if (!this.flag) {
            this.scanTip = '只能一人进行人脸识别'
          }
        }
      }
    },
    plot(rect) {
      // 检测人脸的边框颜色
      this.context.strokeStyle = '#2B96E7'
      this.context.strokeRect(rect.x, rect.y, rect.width, rect.height)
      this.context.font = '11px Helvetica'
      this.context.fillStyle = '#fff'
      this.context.fillText('x: ' + rect.x + 'px', rect.x + rect.width + 5, rect.y + 11)
      this.context.fillText('y: ' + rect.y + 'px', rect.x + rect.width + 5, rect.y + 22)
    },
    // 拍照
    tackPhoto() {
      this.context.drawImage(this.$refs.refVideo, 0, 0, 250, 250)
      // 保存为base64格式
      this.imgUrl = this.saveAsPNG(this.$refs.refCanvas)
      // var formData = new FormData()
      // formData.append('file', this.imgUrl)
      this.scanTip = '登录中，请稍等~'
      this.$store.dispatch('user/facelogin', this.imgUrl).then(res => {
        const name = res.username
        this.$confirm('当前登录用户为：' + name, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '重试',
          type: 'warning',
          center: true
        }).then(() => {
          this.$router.push({ path: this.redirect || '/' })
          this.close()
        }).catch(() => {
          this.retry()
        })
      })
    },
    retry() {
      this.imgUrl = []
      this.tipFlag = false
      this.flag = false
    },
    closeDialog() {
      this.dialogFace = false
      this.imgUrl = []
      this.close()
    },
    // 保存为png,base64格式图片
    saveAsPNG(c) {
      return c.toDataURL('image/jpeg', 0.3)
    },
    // 关闭并清理资源
    close() {
      this.video.srcObject.getTracks()[0].stop()
      this.flag = false
      this.tipFlag = false
      // 关闭摄像头
      tracking.track('#video', this.tracker, { camera: false })
      this.tracker = null
      this.context = null
      this.scanTip = ''
      clearTimeout(this.removePhotoID)
      if (this.streamIns) {
        this.streamIns.enabled = false
        this.streamIns.getTracks()[0].stop()
        this.streamIns.getVideoTracks()[0].stop()
      }
      this.streamIns = null
    }
  }
}
</script>

<style lang="scss" scoped>
#userLayout{
  margin: 0;
  padding: 0;
  background-size: cover;
  width: 100%;
  height: 100%;
  position: relative;
  .login_panle{
    position: absolute;
    top: 3vh;
    left: 2vw;
    width: 96vw;
    height: 94vh;
    background-color: rgba(255,255,255,.8);
    backdrop-filter: blur(5px);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    .login_panle_right{
      background-size: cover;
      width: 40%;
      height: 60%;
      float: right !important;
    }
    .login_panle_form{
      width: 420px;
      background-color: #fff;
      padding: 40px 40px 40px 40px;
      border-radius: 10px;
      box-shadow: 2px 3px 7px  rgba(0,0,0,.2);
      .login_panle_form_title{
        display: flex;
        align-items: center;
        margin: 20px 0;
        .login_panle_form_title_p{
          font-size: 35px;
          padding-left: 20px ;
        }
      }
    }
    .login_panle_foot{
      position: absolute;
      bottom: 20px;
      .links{
        display: flex;
        align-items: center;
        justify-content: space-between;
        .link-icon{
          width: 30px;
          height: 30px;
        }
      }
      .copyright{
        color: #777777;
        margin-top: 5px;
      }
    }
  }
}
//小屏幕不显示右侧，将登陆框居中
@media (max-width: 750px) {
  .login_panle_right{
    display: none;
  }
  .login_panle{
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
  }
  .login_panle_form{
    width: 100%;
  }
}
.camera-wrapper{
    min-height: 400px;
    width: 100%;
    position: relative;
        > * {
            position: absolute;
            left: 0;
            right: 0;
            margin: auto;
        }
        video,
        canvas {
          top: 0;
          border-radius: 50%;
          box-shadow: 0px 0px 12px #66b1ff8a;
        }
  .scanTip{
    top:320px;
    left:100px;
    font-size: 16px;
  }
}
</style>
