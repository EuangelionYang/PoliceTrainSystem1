<template>
  <div class="course-container">
    <el-card>
      <div class="course-label">
        <div class="leftImg">
          <img :src="lessonBrief.cover" class="imgStyle" alt="课程名称">
        </div>
        <div class="rightCon">
          <p class="title">{{ lessonBrief.TrainingName }}</p>
          <p class="teacher">
            <span style="padding-right: 20px">
              <svg-icon icon-class="people" name="mingcheng" />
              {{ lessonBrief.teacher_name }}
            </span>
            <span style="padding-left: 20px ">
              <svg-icon icon-class="people" name="number" />
              {{ lessonBrief.learner_number }}
            </span>
          </p>
          <p class="info">{{ lessonBrief.detail || '暂无简介' }}</p>
        </div>
      </div>
    </el-card>
    <el-card style="margin:20px 0">
      <div class="course-preview">
        <span style="font-size: 14px;color: #999">学习进度</span>
        <div class="learning-process">
          <el-progress :text-inside="true" :stroke-width="15" :percentage="progress" status="success" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {

  props: {
    lessonBrief: {
      type: Object,
      default: Object
    },
    total: {
      type: Object,
      default: Object
    }
  },
  data() {
    return {}
  },
  computed: {
    progress() {
      if ((this.total.complish + this.total.uncomplish) > 0) {
        return parseInt(this.total.complish / (this.total.complish + this.total.uncomplish) * 100)
      } else {
        return 0
      }
    }
  },
  created() {},
  method: {}
}
</script>

<style lang="scss" scoped>
.course-container{
  .course-label {
    min-height: 200px;
    padding: 20px;
    border-radius: 4px;
    margin: -10px;
    display: flex;
    .leftImg {
      width: 300px;
      height: 200px;
      margin: 20px;
      .imgStyle {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        border-radius: 4px;
        position: relative;
      }
    }
    .rightCon {
      width: 70%;
      padding: 20px;
      margin: 10px;
      .title {
        margin-top: 8px;
        font-size: 16px;
        font-weight: 500;
        color: #333;
      }
      .teacher {
        padding: 12px 0;
        color: #999;
        font-size: 12px;
      }
      .info {
        font-size: 14px;
        color: #999;
        line-height: 22px;
        overflow: hidden;
        position: relative;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }
    }
  }
  .course-preview {
    display: flex;
    height: 20px;
    line-height: 20px;
  }
  .learning-process {
    padding-left: 15px;
    width: 90%;
  }
}
</style>
