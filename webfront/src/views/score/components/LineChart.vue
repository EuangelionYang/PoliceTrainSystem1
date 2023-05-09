<template>
  <!--  折线图堆叠  -->
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import * as echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from '../../dashboard/components/mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '300px'
    },
    autoResize: {
      type: Boolean,
      default: true
    },
    chartData: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val)
      }
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
    // 基于准备好的dom，初始化echarts实例
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.setOptions()
    },
    // 绘制图表
    setOptions() {
      this.chart.setOption({
        title: {
          show: true,
          text: '训练历史成绩查看',
          left: 'center',
          textStyle: {
            color: '#000', // 主标题文字的颜色。
            fontStyle: 'normal', // 主标题文字字体的风格。 'normal'  'italic'  'oblique'
            fontWeight: 'bold', // 主标题文字字体的粗细。 'normal' 'bold'  'bolder'  'lighter' 500|600
            fontFamily: 'sans-serif', // 主标题文字的字体系列。
            fontSize: 18, // 字体大小
            lineHeight: '25'
          }
        },
        // x轴参数
        xAxis: {
          data: this.getTimesList(),
          boundaryGap: false,
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 10,
          right: 10,
          bottom: 20,
          top: 30,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        yAxis: {
          axisTick: {
            show: false
          }
        },
        legend: {
          left: 'right',
          data: this.getLegend()
        },
        series: this.getSeries()
      })
    },
    getTimesList() {
      const ans = []
      let num = 0
      this.chartData.forEach(ele => {
        num = ele.grades.length > num ? ele.grades.length : num
      })
      for (let i = 1; i < num + 1; i++) {
        ans.push('第' + i + '次')
      }
      return ans
    },
    getLegend() {
      const ans = []
      this.chartData.forEach(ele => {
        ans.push(ele.chapterName)
      })
      return ans
    },
    getSeries() {
      const ans = []
      this.chartData.forEach(ele => {
        ans.push({
          name: ele.chapterName,
          smooth: true,
          type: 'line',
          data: ele.grades
        })
      })
      return ans
    }
  }
}
</script>
