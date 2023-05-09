<template>
  <div class="register-upload">
    <el-upload
      ref="cardUpload"
      :show-file-list="false"
      :http-request="avatarHttpRequest"
      :on-error="handleError"
      :before-upload="beforeUpload"
      class="avatar-uploader"
      action="#"
    >
      <!-- <div class="el-upload"> -->
      <img
        v-if="imageUrl"
        :src="imageUrl"
        :style="{'width': `${width}px`, 'height': `${width}px`}"
        class="avatar"
      >
      <i
        v-else
        :style="{'width': `${width}px`, 'height': `${width}px`, 'line-height':`${width}px` }"
        class="el-icon-picture avatar-uploader-icon"
      />
      <!-- </div> -->
    </el-upload>
  </div>
</template>

<script>
export default {
  props: {
    imageUrl: {
      type: String,
      required: true,
      default: ''
    },
    width: {
      type: Number,
      default: 80
    }
  },
  data() {
    return {
      // 图片文件，这个需要放在formdata里，所以要返回给父组件,调用emit方法传回去就行
      imgFile: null
    }
  },
  methods: {
    beforeUpload(file) {
      const imageType = ['image/pjpeg', 'image/jpeg', 'image/jpg', 'image/png', 'image/x-png']
      const isJPG = imageType.indexOf(file.type) > -1
      const isLt2M = file.size / 1024 / 1024 < 5
      if (!isJPG) {
        this.$message.error('上传头像图片只能是图片格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 5MB!')
      }
      return isJPG && isLt2M
    },
    avatarHttpRequest(option) {
      this.imgFile = option.file
      // 这里是创建一个临时的url，是为了在修改图片后可以在头像框看到。
      this.$emit('update:imageUrl', URL.createObjectURL(this.imgFile))
      // this.imageUrl = URL.createObjectURL(this.imgFile)
      // // 这里把图片文件传给父组件
      this.$emit('getAvatarFile', this.imgFile)
    },
    handleError() {
      this.$message.error('上传失败')
    }
  }
}
</script>

<style lang="scss">
.register-upload {
  .avatar-uploader {
    display: flex;
    .el-upload {
      cursor: pointer;
      position: relative;
      overflow: hidden;
      // background-color: rgba(0,0,0,0.1);
    }
    .avatar-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 80px;
      height: 80px;
      line-height: 80px;
      text-align: center;
      background-color: rgba(0, 0, 0, 0.1);
    }
    .avatar {
      width: 80px;
      height: 80px;
      display: block;
      object-fit: scale-down;
    }
  }
}

</style>

