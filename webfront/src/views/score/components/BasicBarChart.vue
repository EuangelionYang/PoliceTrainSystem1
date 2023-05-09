<template>
  <div id="BarChart" class="basicBar" style="width: 100%;height: 300px"/>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'BasicBarChart',
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
    // 基础柱状图
    // 初始化echarts实例
    initChart() {
      this.chart = echarts.init(document.getElementById('BarChart'))
      this.chart.setOption({
        title: {
          // 标题
          show: true, // 是否显示
          text: '训练成绩统计表',
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
        // 提示框组件
        tooltip: {
          trigger: 'axis', // 触发类型  'item'图形触发：散点图，饼图等无类目轴的图表中使用； 'axis'坐标轴触发；'none'：什么都不触发。
          axisPointer: { // 坐标轴指示器配置项
            type: 'shadow' // 'line' 直线指示器  'shadow' 阴影指示器  'none' 无指示器  'cross' 十字准星指示器。
          }
        },
        // 调整图表在div容器里的位置，以及图表的背景样式
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true // 设置containLabel: true常用于 防止标签溢出，计算距离时候会计算容器边到标签的距离，否则计算容器边缘到刻度线的距离
        },
        xAxis: [
          {
            type: 'category',
            data: ['训练一', '训练二', '训练三', '训练四', '训练五', '训练六', '训练七'],
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: 'Direct',
            type: 'bar',
            barWidth: '60%',
            data: [40, 50, 60, 70, 80, 90, 100]
          }
        ]
      })
    }
  }
}
</script>

<style scoped>

</style>
