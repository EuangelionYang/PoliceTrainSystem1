<template>
  <div id="PieChart" style="width: 100%;height: 350px"/>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'BasicPieChart',
  props: {
    train_name: {
      type: String,
      default: ''
    },
    score: {
      type: Array,
      default: Array
    }
  },
  data() {
    return {
      chart: null // 定义一个图表
    }
  },
  watch: {
    train_name: {
      handler(newVal, oldVal) {
        if (newVal) {
          this.initChart()
        }
        return newVal
      },
      deep: true
    }
  },
  mounted() {
    // this.$nextTick(() => {
    //   this.initChart()
    // })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    // 基础柱状图
    // 初始化echarts实例
    initChart() {
      this.chart = echarts.getInstanceByDom(document.getElementById('PieChart'))
      if (this.chart === null || this.chart === undefined) {
        this.chart = echarts.init(document.getElementById('PieChart'))
      }
      this.chart.setOption({
        title: {
          text: this.train_name + '-训练成绩分布情况',
          subtext: '注：学员不同成绩区间分布人数',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: this.score,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })
    }
  }
}
</script>

<style scoped>

</style>
