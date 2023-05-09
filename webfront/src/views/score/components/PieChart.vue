<template>
  <!--  饼图-->
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
var echarts = require('echarts')
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
  // 容器销毁时，应调用实例.dispose以销毁实例释放资源，避免内存泄漏。
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
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        // 图例：图表中对内容区元素的注释
        legend: {
          left: 'center',
          bottom: '10',
          data: ['I', 'T', 'F', 'G', 'E']
        },
        series: [
          {
            name: 'WEEKLY TRAIN',
            type: 'pie',
            roseType: 'radius',
            radius: [15, 95],
            center: ['50%', '38%'],
            // data里每一个项就是数据项（dataItem）
            data: [
              // value指数据项的数据值
              { value: 320, name: 'I' },
              { value: 240, name: 'T' },
              { value: 149, name: 'F' },
              { value: 100, name: 'G' },
              { value: 59, name: 'E' }
            ],
            animationEasing: 'cubicInOut',
            animationDuration: 2600
          }
        ]
      })
    }
  }
}
</script>
