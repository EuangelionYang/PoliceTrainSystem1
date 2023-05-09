<template>
  <div class="app-container">
    <Brief :lesson-brief="lessonBrief" :total="total"/>
    <div class="course-tab">
      <el-card>
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="课程介绍" name="intro">
            <p class="detail">{{ lessonBrief.detail || '暂无简介' }}</p>
          </el-tab-pane>
          <el-tab-pane label="课程目录" name="catalogue">
            <div class="catalogue" style="display: flex;min-height: 600px">
              <div v-infinite-scroll="load" class="chap" style="overflow-x:hidden;width: 20%">
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
                <Player v-if="isPlay" :movie-src="movieSrc" @handleFinish="handleFinish"/>
                <span v-else description="请选择视频"/>
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
          <el-tab-pane label="课程成绩" name="grade">
            <div class="grade">
              <el-row :gutter="20">
                <el-col :span="10">
                  <div class="leftInfo">
                    <p>总成绩</p>
                    <pie-grade v-if="isShow" :grade="totalGrade" :total="total"/>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="rightInfo">
                    <p>成绩明细</p>
                    <el-collapse v-model="activeNames">
                      <el-collapse-item title="视频单元考核" name="1">
                        <div class="videoList">
                          <ul style="list-style-type: none">
                            <li v-for="(chap,index) in chapterList" :key="chap.id" :index="chap.id+''"
                                style="padding: 10px">
                              <span>视频{{ index + 1 }}</span>
                              <div class="chapterTitle" style="padding-top: 10px;display: flex">
                                <div class="titleLeft" style="width: 60%">
                                  <span class="svg-container">
                                    <svg-icon icon-class="play"/>
                                  </span>
                                  <span>{{ chap.chapterTitle }}</span>
                                </div>
                                <div class="titleMiddle" style="width: 20%">
                                  <div v-if="chap.is_finish">
                                    <span class="svg-container">
                                      <svg-icon icon-class="finish"/>
                                    </span>
                                    <span>已完成</span>
                                  </div>
                                  <div v-else>
                                    <span class="svg-container">
                                      <svg-icon icon-class="unfinish"/>
                                    </span>
                                    <span>未完成</span>
                                  </div>
                                </div>
                                <div class="titleRight" style="width: 20%">
                                  <span>{{ chap.grade }}分</span>
                                </div>
                              </div>
                            </li>
                          </ul>
                        </div>
                      </el-collapse-item>
                    </el-collapse>
                  </div>
                </el-col>
              </el-row>
              <el-row style="padding-top: 20px">
                <el-col :span="24">
                  <line-chart v-if="isShow" :chart-data="chapterGrades"/>
                </el-col>
              </el-row>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<script>
import {getOneTraining} from '@/api/lesson/lessonList'
import {getChapterList} from '@/api/lesson/chapter'
import {getChapterGrade, getChapterHistoryGrade, submitChapterGrade} from '@/api/lesson/study'
import Brief from '@/views/lesson/study/detail/components/Brief'
import Player from '@/views/lesson/study/detail/components/VideoPlayer'
import PieGrade from '@/views/score/components/PieGrade'
import {mapGetters} from 'vuex'
import LineChart from '@/views/score/components/LineChart.vue'

export default {
  name: 'StudyDetail',
  components: {Player, Brief, PieGrade, LineChart},
  data() {
    return {
      activeName: 'intro',
      activeNames: ['1'],
      param: '', // 要传递的参数
      isPlay: false,
      lessonBrief: {},
      chapterList: [],
      nowTab: 'Intro',
      load: true,
      movieSrc: '',
      chapterGrades: [],
      totalGrade: 0,
      total: {
        complish: 0,
        uncomplish: 0
      },
      isShow: false,
      chapterId: -1,
      video_title: null,
      video_details: null,
      video_sex: null,
      video_crime_type: null,
      video_age: null,
      video_crime_tendency: null,
      video_mental: null,
      video_emotion: null,
      video_type: null,
      lessonType: null
    }
  },
  computed: {
    ...mapGetters(['id'])
  },
  created() {
    this.getLessonDetail()
    this.getTrainingChapter()
    this.getEachGrade()
  },
  methods: {
    activeKeyframe(item) {
      this.active_keyframe.id = item.id
      this.active_keyframe.keyframe_Description = item.keyframe_Description
      this.active_keyframe.keyframe_time = item.keyframe_time
      this.skipTime(item.keyframe_time / 1000)
      // alert(this.current)
      this.active_keyframe.keyframe_Focus = item.keyframe_Focus
      this.active_keyframe.chapter = item.chapter
      this.active_keyframe.is_edit = true
      for (let base = 0; base < 10; base++) {
        // console.log(2 ** base)
        if ((item.keyframe_Focus & (2 ** base)) > 0) {
          this.checked[base] = true
        } else {
          this.checked[base] = false
        }
      }
    },
    resetKeyframe() {
      this.checked = [false, false, false, false, false, false, false, false, false, false]
    },
    submitKeyframe() {
      let focus = 0
      for (let base = 0; base < 10; base++) {

        if (this.checked[base] === true) {
          focus += (2 ** base)
        }
      }
      this.active_keyframe.keyframe_Focus = focus
      editChapterKeyframe(this.active_keyframe.id, {
        keyframe_Description: this.active_keyframe.keyframe_Description,
        keyframe_time: this.active_keyframe.keyframe_time,
        keyframe_Focus: this.active_keyframe.keyframe_Focus,
        chapter: this.active_keyframe.chapter
      }).then(() => {
        this.$message.success('提交成功')
      }).finally(
        () => {
          this.getKeyframe()
        }
      )
    },
    getKeyframe() {
      getChapterKeyframe({chapter_id: this.videoChapterId}).then(res => {
        this.keyframeList = res
      })
    },
    generateKeyframe() {
      if (this.keyframeList.length !== 0) {

      } else {
        this.keyframe_loading = true
        generateChapterKeyframe({chapter_id: this.videoChapterId}).then(() => {
          this.$message.success('生成关键帧成功')
          this.keyframe_loading = false
        }).finally(() => {
          this.getKeyframe()
          this.keyframe_loading = false
        })
      }
    },
    getLessonDetail() {
      getOneTraining(this.$route.query.id).then(res => {
        this.lessonBrief = res
        this.lessonType = res.category
        // console.log(res.category)
      })
    },
    getTrainingChapter() {
      getChapterList({training_id: this.$route.query.id}).then(res => {
        this.chapterList = res
      }).then(() => {
        const params = {
          training_id: this.$route.query.id,
          learner_id: this.id
        }
        getChapterGrade(params).then(res => {
          res.chapters.forEach((ele, index) => {
            this.chapterList[index].is_finish = ele.is_finish
            this.chapterList[index].grade = ele.grade
            this.totalGrade += ele.grade
            if (this.chapterList[index].is_finish) {
              this.total.complish += 1
            } else {
              this.total.uncomplish += 1
            }
          })
        })
      })
    },
    getEachGrade() {
      const params = {
        training_id: this.$route.query.id,
        learner_id: this.id
      }
      getChapterHistoryGrade(params).then(res => {
        this.chapterGrades = res.chapters
      })
    },
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
      // console.log(data)
    },
    handleClick(tab, event) {
      if (tab.name === 'grade') {
        this.isShow = true
      }
    },
    handleFinish() {
      const params = {
        chapter_id: this.chapterId,
        learner_id: this.id,
        grade: Math.round(Math.random() * 100)
      }
      submitChapterGrade(params).then(() => {
        this.$message.success('该视频已看完！')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.el-scrollbar__wrap {
  overflow-x: hidden;
}

.course-tab {
  height: 700px;

  .detail {
    line-height: 30px;
    text-indent: 30px;
  }
}

.grade {
  width: 100%;

  .leftInfo {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    height: 320px;
  }

  .rightInfo {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    height: 320px;

    .el-collapse-item {
      overflow: auto;
      height: 250px;
    }
  }

  .svg-container {
    padding-right: 5px;
  }
}

.box-card {
  width: 23%;
}
</style>
