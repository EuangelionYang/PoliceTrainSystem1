<template>
  <div class="r-echarts-line">
    <div v-if="flag === false" class="top">
      <div class="select-list">
        <el-row>
          <!-- <el-col :span="8">
            <el-input
              v-model="searchInfo"
              placeholder="请输入学员名称"
              clearable
              @keyup.enter.native="getAllCharts('search')"
              @clear="getAllCharts()"
            />
          </el-col>
          <el-col :span="1.5">
            <el-button type="primary" icon="el-icon-search">搜索</el-button>
          </el-col> -->
          <span>学员：</span>
          <el-select v-model="selectedStudent" placeholder="请选择学员" @change="handleChange(selectedStudent)">
            <el-option v-for="(item,index) in learners" :key="index" :label="item.name" :value="item.id"/>
          </el-select>
        </el-row>
      </div>
    </div>
    <div v-if="selectedStudent === null && flag === false" class="empty">
      <div>
        <img :src="emptyImg" alt="暂无数据">
      </div>
      <p style="color:#B0AFAF">暂无数据,请先选择学员</p>
    </div>
    <div v-else class="bottom">
      <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
        <bar-dotted :stu_detail="train_detail"/>
      </el-row>
    </div>
  </div>
</template>

<script>
import BarDotted from '@/views/score/components/BarDotted'
import PieChart from '@/views/score/components/PieChart'
import RadarChart from '@/views/score/components/RadarChart'
import { mapGetters } from 'vuex'
import imgUrl from '@/assets/images/empty.svg'
import { getOneLearnerGrade } from '@/api/score/score'
import { getLearners } from '@/api/lesson/lessonList'

export default {
  name: 'Index',
  components: { BarDotted, PieChart, RadarChart },
  data() {
    return {
      searchInfo: '',
      selectedStudent: null,
      flag: false,
      emptyImg: imgUrl,
      learners: [],
      train_detail: {
        train_scores: [],
        train_names: [],
        stu_name: ''
      }
    }
  },
  computed: {
    ...mapGetters(['identifier', 'id'])
  },
  created() {
    this.identifier.forEach(ele => {
      if (ele === 'student') {
        this.flag = true
        this.getScore(this.id)
      } else {
        this.getStudents()
      }
    })
  },
  methods: {
    getScore(id) {
      getOneLearnerGrade({ user_id: id }).then(res => {
        this.train_detail.train_scores = []
        this.train_detail.train_names = []
        this.train_detail.stu_name = res.name
        if (res.trainings.length === 0) {
          this.$message.error('该生暂无成绩，请选择其他学员！')
        } else {
          res.trainings.forEach(ele => {
            this.train_detail.train_names.push(ele.training)
            this.train_detail.train_scores.push(ele.grade)
          })
        }
      })
    },
    getStudents() {
      getLearners().then(res => {
        this.learners = res
      })
    },
    handleChange(value) {
      this.getScore(value)
    }
  }
}
</script>

<style scoped>
.r-echarts-line{
  padding: 20px;
}
.empty{
  text-align: center;
  padding-top: 50px
}
</style>
