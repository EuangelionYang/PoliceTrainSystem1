<template>
  <div class="app-container">
    <Brief :lesson-brief="lessonBrief" :total="total" />
    <div class="course-tab">
      <el-card>
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="课程介绍" name="intro">
            <p class="detail">{{ lessonBrief.detail || '暂无简介' }}</p>
          </el-tab-pane>
          <el-tab-pane label="课程目录" name="catalogue">
            <div class="catalogue" style="display: flex;height: 600px">
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
                          <svg-icon icon-class="play" />
                          <!--<svg-icon v-if="chap.is_finish" icon-class="finish" />-->
                          <!--<svg-icon v-else icon-class="unfinish" />-->
                        </span>
                        {{ chap.chapterTitle }}
                      </el-menu-item>
                    </el-submenu>
                  </el-menu>
                </div>
              </div>
              <div class="player" style="width:65%;margin: 50px">
                <Player v-if="isPlay" :movie-src="movieSrc" @handleFinish = "handleFinish" />
                <span v-else description="请选择视频" />
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="课程成绩" name="grade">
            <div class="grade">
              <el-row :gutter="20">
                <el-col :span="10">
                  <div class="leftInfo">
                    <p>总成绩</p>
                    <pie-grade v-if="isShow" :grade="totalGrade" :total="total" />
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="rightInfo">
                    <p>成绩明细</p>
                    <el-collapse v-model="activeNames">
                      <el-collapse-item title="视频单元考核" name="1">
                        <div class="videoList" >
                          <ul style="list-style-type: none">
                            <li v-for="(chap,index) in chapterList" :key="chap.id" :index="chap.id+''" style="padding: 10px">
                              <span>视频{{ index + 1 }}</span>
                              <div class="chapterTitle" style="padding-top: 10px;display: flex">
                                <div class="titleLeft" style="width: 60%">
                                  <span class="svg-container">
                                    <svg-icon icon-class="play" />
                                  </span>
                                  <span>{{ chap.chapterTitle }}</span>
                                </div>
                                <div class="titleMiddle" style="width: 20%">
                                  <div v-if="chap.is_finish">
                                    <span class="svg-container">
                                      <svg-icon icon-class="finish" />
                                    </span>
                                    <span>已完成</span>
                                  </div>
                                  <div v-else>
                                    <span class="svg-container">
                                      <svg-icon icon-class="unfinish" />
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
                  <line-chart v-if="isShow" :chart-data="chapterGrades" />
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
import { getOneTraining } from '@/api/lesson/lessonList'
import { getChapterList } from '@/api/lesson/chapter'
import { getChapterGrade, getChapterHistoryGrade, submitChapterGrade } from '@/api/lesson/study'
import Brief from '@/views/lesson/study/detail/components/Brief'
import Player from '@/views/lesson/study/detail/components/VideoPlayer'
import PieGrade from '@/views/score/components/PieGrade'
import { mapGetters } from 'vuex'
import LineChart from '@/views/score/components/LineChart.vue'

export default {
  name: 'StudyDetail',
  components: { Player, Brief, PieGrade, LineChart },
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
      chapterId: -1
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
    getLessonDetail() {
      getOneTraining(this.$route.query.id).then(res => {
        this.lessonBrief = res
        this.training_id = res.id
      })
    },
    getTrainingChapter() {
      getChapterList({ training_id: this.$route.query.id }).then(res => {
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
.grade{
  width: 100%;
  .leftInfo{
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    height: 320px;
  }
  .rightInfo{
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    height: 320px;
    .el-collapse-item{
      overflow:auto;
      height: 250px;
    }
  }
  .svg-container{
    padding-right: 5px;
  }
}

</style>
