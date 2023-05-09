<template>
  <!--  堆叠柱状图-->
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import * as echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from '../../dashboard/components/mixins/resize'

const animationDuration = 6000

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
    }
  },
  data() {
    return {
      chart: null
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
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.chart.setOption({
        title: {
          show: true,
          text: '训练统计情况',
          left: 'center',
          textStyle: {
            color: '#000', // 主标题文字的颜色。
            fontStyle: 'normal', // 主标题文字字体的风格。 'normal'  'italic'  'oblique'
            fontWeight: 'bold', // 主标题文字字体的粗细。 'normal' 'bold'  'bolder'  'lighter' 500|600
            fontFamily: 'sans-serif', // 主标题文字的字体系列。
            fontSize: 18, // 字体大小
            lineHeight: '30'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          top: 10,
          left: '2%',
          right: '2%',
          bottom: '3%',
          containLabel: true
        },
        // x轴参数
        xAxis: [{
          type: 'category',
          data: ['擒拿', '体能', '记忆力', '射击', '格斗', '组枪'],
          // 轴线刻度
          axisTick: {
            alignWithLabel: true
          }
        }],
        yAxis: [{
          type: 'value',
          axisTick: {
            show: false
          }
        }],
        series: [{
          name: 'lessonA',
          type: 'bar',
          stack: 'vistors',
          barWidth: '60%',
          data: [79, 52, 200, 334, 390, 220],
          animationDuration
        }, {
          name: 'lessonB',
          type: 'bar',
          stack: 'vistors',
          barWidth: '60%',
          data: [80, 52, 200, 334, 390, 220],
          animationDuration
        }, {
          name: 'lessonC',
          type: 'bar',
          stack: 'vistors',
          barWidth: '60%',
          data: [30, 52, 200, 334, 330, 220],
          animationDuration
        }]
      })
    }
  }
}
</script>
