<template>
  <div class="app-container check-container">
    <!--    训练简介区域-->
    <el-card>
      <div class="course-label">
        <div class="leftInfo">
          <div class="leftImg">
            <img :src="lessonBrief.cover" class="imgStyle" alt="课程封面">
          </div>
          <div v-if="lessonBrief.is_publish" class="remove">
            <svg-icon icon-class="publish" style="width: 100px;height: 100px" name="publish"/>
          </div>
        </div>
        <div class="middleInfo">
          <p class="title">{{ lessonBrief.TrainingName }}</p>
          <p class="teacher">
            <span style="padding-right: 20px">
              <svg-icon icon-class="teacher" name="mingcheng"/>
              {{ lessonBrief.teacher_name }}
            </span>
            <span style="padding-left: 20px ">
              <svg-icon icon-class="people" name="number"/>
              {{ lessonBrief.learner_number }}
            </span>
            <el-button class="set-students" type="text" @click="handleSet()">设置学员</el-button>
          </p>
          <p class="info">{{ lessonBrief.detail || '暂无简介' }}</p>
        </div>
        <div class="rightPart">
          <div class="checkCon">
            <svg-icon v-if="lessonBrief.is_review" icon-class="checked" style="width: 100px;height: 100px"
                      name="checked"/>
            <svg-icon v-else icon-class="uncheck" style="width: 100px;height: 100px" name="uncheck"/>
          </div>
          <div class="handleBtn">
            <!-- <el-button v-if="!role" @click="previous">返回修改</el-button> -->
            <div v-if="role">
              <el-button v-if="!lessonBrief.is_review" @click="pass()">通过审核</el-button>
              <el-button v-if="lessonBrief.is_review" @click="cancelPass()">取消通过</el-button>
              <el-button v-else @click="notPass()">不通过</el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>
    <!--    章节目录区域-->
    <el-tabs type="border-card" style="margin-top: 20px">
      <el-tab-pane label="课程目录">
        <div class="catalogue" style="display: flex;height: 100% ;min-height: 600px">
          <div v-infinite-scroll="load" class="chap" style="overflow-x:hidden;width: 20%">
            <!--            <ChapterList :chapter-list="chapterList" @getWhichVideo="getWhichVideo"/>-->
            <div class="chapterList">
              <el-menu
                :default-active="chapterList.index"
                class="el-menu-vertical-demo"
              >
                <el-submenu v-for="(chap,index) in chapterList" :key="chap.id" :index="chap.id+''">
                  <template slot="title">
                    <span>视频{{ index + 1 }} {{ chap.chapterTitle }}</span>
                  </template>
                  <el-menu-item :index="chap.chapterTitle" @click="getWhichVideo(chap)">
                        <span class="svg-container" style="padding-right: 8px">
                          <svg-icon icon-class="play"/>
                          <!--<svg-icon v-if="chap.is_finish" icon-class="finish" />-->
                          <!--<svg-icon v-else icon-class="unfinish" />-->
                        </span>
                    {{ chap.chapterTitle }}
                  </el-menu-item>
                </el-submenu>
              </el-menu>
            </div>

          </div>
          <div class="player" style="width:50%;margin: 50px">
            <Player v-if="isPlay" :movie-src="movieSrc"/>
            <!-- <el-empty v-else description="请选择章节" /> -->
          </div>
          <el-card class="box-card">
            <span>课程名称: {{ video_title }}<br><br></span>
            <span v-if="lessonType===2">性别: {{ video_sex }}<br><br></span>
            <span v-if="lessonType===2">犯罪类型: {{ video_crime_type }}<br><br></span>
            <span v-if="lessonType===2">年纪: {{ video_age }}<br><br></span>
            <span v-if="lessonType===2">犯罪倾向: {{ video_crime_tendency }}<br><br></span>
            <span v-if="lessonType===2">精神状态: {{ video_mental }}<br><br></span>
            <span v-if="lessonType===2">犯罪情绪: {{ video_emotion }}<br><br></span>
            <span v-if="lessonType===2">课程类型: {{ video_type }}<br><br></span>
            <span v-if="lessonType===3">性别: {{ video_sex }}<br><br></span>
            <span v-if="lessonType===3">犯罪类型: {{ video_crime_type }}<br><br></span>
            <span v-if="lessonType===3">年纪: {{ video_age }}<br><br></span>
            <span v-if="lessonType===3">犯罪倾向: {{ video_crime_tendency }}<br><br></span>
            <span v-if="lessonType===3">精神状态: {{ video_mental }}<br><br></span>
            <span v-if="lessonType===3">犯罪情绪: {{ video_emotion }}<br><br></span>
            <span v-if="lessonType===3">课程类型: {{ video_type }}<br><br></span>
            <span>课程描述: {{ video_details }}</span>
          </el-card>
        </div>

      </el-tab-pane>
    </el-tabs>
    <el-dialog :visible="openDialog" title="设置学员" width="720px" custom-class="training-dialog" @close="cancel">
      <el-form ref="dialogForm" :model="dialogForm">
        <el-form-item>
          <el-transfer
            v-model="dialogForm.learners"
            :titles="['学员名单', '已选中']"
            :props="{
              key: 'id',
              label: 'name'
            }"
            :data="userList"
            filterable
            filter-placeholder="请输入学员名字"
          />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" @click="onSubmit()">提 交</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {getOneTraining, doReview, getLearners, setTrainingLearners} from '@/api/lesson/lessonList'
import {getChapterList} from '@/api/lesson/chapter'
import ChapterList from '@/views/lesson/study/detail/components/ChapterList'
import Player from '@/views/lesson/study/detail/components/VideoPlayer'
import {mapGetters} from 'vuex'

export default {
  components: {Player, ChapterList},
  data() {
    return {
      video_title: '',
      video_details: '',
      video_sex: '',
      video_crime_type: '',
      video_age: '',
      video_crime_tendency: '',
      video_mental: '',
      video_emotion: '',
      video_type: '',
      lessonType: '',
      openDialog: false,
      dialogForm: {
        learners: []
      },
      load: true,
      role: false,
      check: 1,
      lessonBrief: {},
      isPlay: false,
      movieSrc: '',
      userList: [],
      chapterList: []
    }
  },
  computed: {
    ...mapGetters(['roles', 'identifier'])
  },
  mounted() {
    // 监听playMovie事件
    // this.$bus.$on('playMovie', ({ url }) => {
    //   this.isPlay = true
    //   this.movie_src = url
    // })
  },
  created() {
    this.getCoursePublishId()
    this.getStudents()
    this.getTrainingChapter()
    this.identifier.forEach(ele => {
      if (ele === 'education') {
        this.role = true
      }
    })
  },
  methods: {
    getCoursePublishId() {
      getOneTraining(this.$route.query.id).then(res => {
        this.lessonBrief = res
        this.dialogForm.learners = res.learners
        this.lessonType = res.category
      })
    },
    getStudents() {
      getLearners().then(res => {
        this.userList = res
      })
    },
    getTrainingChapter() {
      getChapterList({training_id: this.$route.query.id}).then(res => {
        this.chapterList = res
      })
    },
    // 返回编辑
    // previous() {
    //   if (this.lessonBrief.is_publish) {
    //     this.$message.error('该训练已发布，不能进行修改')
    //     return
    //   } else {
    //     this.$router.push({ path: '/upload', query: { id: this.$route.query.id }})
    //   }
    // },
    // 通过审核
    pass() {
      this.check = 1
      const params = {
        training_id: this.$route.query.id,
        is_pass: this.check
      }
      doReview(params).then(() => {
        this.$message.success('该训练已通过审核')
      }).finally(() => {
        this.$router.replace({path: 'lessonList'})
      })
    },
    // 审核不合格驳回
    notPass() {
      this.check = 0
      const params = {
        training_id: this.$route.query.id,
        is_pass: this.check
      }
      doReview(params).then(() => {
        this.$message.success('该训练未通过审核')
      }).finally(() => {
        this.$router.replace({path: 'lessonList'})
      })
    },
    cancelPass() {
      this.check = 0
      const params = {
        training_id: this.$route.query.id,
        is_pass: this.check
      }
      doReview(params).then(() => {
        this.$message.success('该训练取消通过审核')
      }).finally(() => {
        this.$router.replace({path: 'lessonList'})
      })
    },
    handleSet() {
      this.openDialog = true
    },
    onSubmit() {
      const params = {
        training_id: this.$route.query.id,
        learner_ids: this.dialogForm.learners
      }
      setTrainingLearners(params).then(() => {
        this.$message.success('学员设置成功')
      }).finally(() => {
        this.getCoursePublishId()
        this.cancel()
      })
    },
    cancel() {
      this.openDialog = false
      this.$refs.dialogForm.resetFields()
      this.dialogForm.learners = this.lessonBrief.learners
    },
    // getWhichVideo(data) {
    //   console.log(data)
    //   this.movieSrc = data
    //   this.isPlay = true
    // }
    getWhichVideo(data) {
      this.chapterId = data.id
      this.movieSrc = data.chapterFile
      this.isPlay = true
      this.video_title = data.chapterTitle
      this.video_sex = data.sex
      this.video_crime_type = data.crime_type
      this.video_age = data.age
      this.video_crime_tendency = data.crime_tendency
      this.video_mental = data.mental
      this.video_emotion = data.emotion
      this.video_type = data.type
      this.video_details = data.details
      console.log(data)
    },
  }
}
</script>
<style lang="scss" scoped>
.check-container {
  min-width: 800px;

  .course-label {
    min-height: 200px;
    border-radius: 4px;
    display: flex;
    justify-content: center;

    .leftInfo {
      position: relative;
      margin: 20px;

      .leftImg {
        width: 300px;
        height: 200px;
        position: relative;
        text-align: center;

        .imgStyle {
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
          border-radius: 4px;
        }
      }

      .remove {
        position: absolute;
        top: 0;
        left: 200px;
        z-index: 2;
      }
    }

    .middleInfo {
      width: 40%;
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

        .set-students {
          padding-left: 15px;
        }
      }

      .info {
        font-size: 14px;
        color: #999;
        line-height: 22px;
        height: 66px;
        overflow: hidden;
        position: relative;
      }

    }

    .rightPart {
      width: 20%;

      .checkCon {
        margin-top: 30px;
      }

      .handleBtn {
        padding-top: 15px;

        .el-button {
          margin-bottom: 5px;
        }
      }
    }
  }
}

.box-card {
  width: 23%;
}
</style>
<style lang="scss">
.training-dialog {
  .el-input__count {
    top: 75px;
    right: 25px;
    line-height: 15px;
  }

  .el-transfer-panel {
    width: 300px;
  }

  .el-transfer__buttons {
    width: 80px;
    padding: 10px;

    .el-transfer__button {
      margin: 10px 0px;
    }
  }
}
</style>
