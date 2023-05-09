<template>
  <div id="BarDotted" class="BarDotted" style="width: 100%;height: 300px"/>
</template>
<script>
import * as echarts from 'echarts'

export default {
  name: 'BarDotted',
  props: {
    stu_detail: {
      type: Object,
      default: Object
    }
  },
  data() {
    return {
      chart: null, // 定义一个图表
      category: [],
      dottedBase: '',
      // lineData: [45, 55, 75, 95, 100, 65, 78, 59, 80, 98],
      barData: [],
      stu_name: ''
    }
  },
  watch: {
    stu_detail: {
      handler(newVal, oldVal) {
        if (newVal) {
          this.category = newVal.train_names
          this.barData = newVal.train_scores
          this.stu_name = newVal.stu_name
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
      this.chart = echarts.init(document.getElementById('BarDotted'))
      this.chart.setOption({
        backgroundColor: '#0f375f',
        title: {
          text: this.stu_name + '-训练成绩统计分析图',
          left: 'center',
          textStyle: {
            color: '#ccc'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          // data: ['平均成绩', '训练成绩'],
          data: ['训练成绩'],
          right: 'right',
          textStyle: {
            color: '#ccc'
          }
        },
        xAxis: {
          data: this.category,
          axisLine: {
            lineStyle: {
              color: '#ccc'
            }
          }
        },
        yAxis: {
          splitLine: { show: false },
          axisLine: {
            lineStyle: {
              color: '#ccc'
            }
          }
        },
        series: [
          {
            name: '平均成绩',
            type: 'line',
            smooth: true,
            showAllSymbol: true,
            symbol: 'emptyCircle',
            symbolSize: 15,
            data: this.lineData
          },
          {
            name: '训练成绩',
            type: 'bar',
            barWidth: 10,
            itemStyle: {
              borderRadius: 5,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#14c8d4' },
                { offset: 1, color: '#43eec6' }
              ])
            },
            data: this.barData
          }
          // {
          //   name: 'line',
          //   type: 'bar',
          //   barGap: '-100%',
          //   barWidth: 10,
          //   itemStyle: {
          //     color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          //       { offset: 0, color: 'rgba(20,200,212,0.5)' },
          //       { offset: 0.2, color: 'rgba(20,200,212,0.2)' },
          //       { offset: 1, color: 'rgba(20,200,212,0)' }
          //     ])
          //   },
          //   z: -12,
          //   data: this.lineData
          // },
          // {
          //   name: 'dotted',
          //   type: 'pictorialBar',
          //   symbol: 'rect',
          //   itemStyle: {
          //     color: '#0f375f'
          //   },
          //   symbolRepeat: true,
          //   symbolSize: [12, 4],
          //   symbolMargin: 1,
          //   z: -10,
          //   data: this.lineData
          // }
        ]

      })
    }
  }
}
</script>

<style scoped>

</style>
