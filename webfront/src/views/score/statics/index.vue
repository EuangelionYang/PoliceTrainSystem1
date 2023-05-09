<template>
  <div class="r-echarts-line">
    <div class="top">
      <div class="select-list">
        <el-row :gutter="20">
          <el-col :span="8">
            <span>训练：</span>
            <el-select v-model="trainID" filterable placeholder="训练名称" @change="getAllCharts()">
              <el-option v-for="(item,index) in trainList" :key="index" :label="item.TrainingName" :value="item.id"/>
            </el-select>
          </el-col>
        </el-row>
      </div>
    </div>
    <div v-if="trainID === null" class="empty">
      <div>
        <img :src="emptyImg" alt="暂无数据">
      </div>
      <p style="color:#B0AFAF">暂无数据,请先选择训练</p>
    </div>
    <div v-loading="chartLoading" v-else class="bottom">
      <el-row :gutter="20">
        <el-card class="chart-card">
          <el-col :span="12">
            <div class="chart-wrapper">
              <basic-pie-chart :train_name="train_name" :score="score_table" />
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-wrapper">
              <ring-gauge :score="finish_table" :train_name="train_name"/>
            </div>
          </el-col>
        </el-card>
      </el-row>
      <el-row style="margin-top:20px">
        <el-col :span="24">
          <el-card class="table-card">
            <h3>{{ train_detail.TrainingName }}-训练成绩详情</h3>
            <el-table :ref="score_detail" :data="score_detail">
              <el-table-column label="学生姓名" prop="name"/>
              <el-table-column label="成绩" prop="grade">
                <template slot-scope="scope">
                  {{ scope.row.grade || '暂无成绩' }}
                </template>
              </el-table-column>
              <el-table-column label="完成情况" prop="is_finish">
                <template slot-scope="scope">
                  <span v-if="scope.row.is_finish === true">
                    {{ scope.row.finish }}
                    <i class="el-icon-success" style="color:#67c23a"/>
                  </span>
                  <span v-else>
                    {{ scope.row.finish }}
                    <i class="el-icon-error" style="color:#f56c6c"/>
                  </span>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import BasicPieChart from '@/views/score/components/BasicPieChart'
import RingGauge from '@/views/score/components/RingGauge'
import imgUrl from '@/assets/images/empty.svg'
import { getLearnersGrade } from '@/api/score/score'
import { getTrainingListByTeacher, getTrainingListByEducation } from '@/api/lesson/lessonList'
import { mapGetters } from 'vuex'

export default {
  name: 'Stat',
  components: { BasicPieChart, RingGauge },
  data() {
    return {
      trainID: null,
      emptyImg: imgUrl,
      trainList: [],
      train_detail: {},
      train_name: null,
      finish_table: [
        { name: '已完成', value: 0 },
        { name: '未完成', value: 0 }
      ],
      score_detail: [],
      score_table: [
        { value: 0, name: '90以上' },
        { value: 0, name: '80-90' },
        { value: 0, name: '70-80' },
        { value: 0, name: '60-70' },
        { value: 0, name: '低于60' }
      ],
      chartLoading: true
    }
  },
  computed: {
    ...mapGetters(['identifier', 'id'])
  },
  created() {
    this.identifier.forEach(ele => {
      if (ele === 'education') {
        this.role = true
      } else if (ele === 'teacher') {
        this.role = false
      }
    })
    this.getTrains()
  },
  methods: {
    getTrains() {
      if (this.role === true) {
        getTrainingListByEducation({ no_page: 1 }).then(res => {
          this.trainList = res
        })
      } else {
        getTrainingListByTeacher({ teacher_id: this.id, no_page: 1 }).then(res => {
          this.trainList = res
        })
      }
    },
    getAllCharts() {
      if (this.trainID !== null) {
        this.chartLoading = true
        getLearnersGrade({ training_id: this.trainID }).then(res => {
          this.train_detail = res
          this.train_name = res.TrainingName
          this.finish_table[0].value = Number(res.learners.finish)
          this.finish_table[1].value = Number(res.learners.total) - Number(res.learners.finish)
          this.score_detail = res.learners.detail
          this.score_table.forEach(ele => {
            ele.value = 0
          })
          res.learners.detail.forEach(ele => {
            if (ele.grade < 60) {
              this.score_table[4].value += 1
            } else if (ele.grade >= 60 && ele.grade < 70) {
              this.score_table[3].value += 1
            } else if (ele.grade >= 70 && ele.grade < 80) {
              this.score_table[2].value += 1
            } else if (ele.grade >= 80 && ele.grade < 90) {
              this.score_table[1].value += 1
            } else {
              this.score_table[0].value += 1
            }
          })
        }).finally(() => {
          this.chartLoading = false
        })
      }
    }
  }
}
</script>

<style scoped>
.r-echarts-line{
  padding: 20px;
}
.bottom{
  padding-top: 20px;
}
.empty{
  text-align: center;
  padding-top: 50px
}
.chart-card{
  height: 360px;
}
.table-card{
  min-height: 400px;
}
</style>
