<template>
  <div id="pieGrade" class="pieGrade" style="width: 300px;height: 300px" />
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'PieGrade',
  props: {
    grade: {
      type: Number,
      default: 0
    },
    total: {
      type: Object,
      default: Object
    }
  },
  data() {
    return {
      chart: null // 定义一个图表
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    // 得分成绩饼图
    // 初始化echarts实例
    initChart() {
      this.chart = echarts.init(document.getElementById('pieGrade'))
      this.chart.setOption({
      // 提示框
        tooltip: {
          trigger: 'item',
          // formatter设置提示框显示内容
          // {a}指series.name  {b}指series.data的name
          // {c}指series.data的value  {d}%指这一部分占总数的百分比
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        color: ['#27D9C8', '#D8D8D8'],
        title: {
          text: '平均得分',
          subtext: String(this.grade),
          left: 'center',
          top: 'center',
          textStyle: {
            color: '#333',
            fontSize: 25,
            align: 'center'
          },
          // 副标题文本样式设置
          subtextStyle: {
            fontSize: 30,
            color: '#27D9C8'
          }
        },
        series: [{
          name: '当前训练', // 系列名称
          type: 'pie', // 系列类型
          radius: ['60%', '70%'], // 饼图的半径，数组的第一项是内半径，第二项是外半径。[ default: [0, '75%'] ]
          label: { // 饼图图形上的文本标签，可用于说明图形的一些数据信息，比如值，名称等.
            normal: {
              show: false, // 是否显示标签[ default: false ]
              position: 'center'
            }
          },
          data: [ // 系列中的数据内容数组。
            { name: '已完成', value: this.total.complish },
            { name: '未完成', value: this.total.uncomplish }
          ]
        }]
      })
    }
  }
}
</script>

<style scoped>

</style>
