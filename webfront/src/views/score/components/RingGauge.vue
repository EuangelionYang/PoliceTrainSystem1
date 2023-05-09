<template>
  <div id="ringChart" class="ringGauge" style="width: 100%;height: 300px"/>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'RingGauge',
  props: {
    score: {
      type: Array,
      default: Array
    },
    train_name: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      chart: null, // 定义一个图表
      pieData: [
        { name: '已完成', value: 0 },
        { name: '未完成', value: 0 }
      ]
    }
  },
  watch: {
    score: {
      handler(newVal, oldVal) {
        if (newVal) {
          this.pieData = newVal
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
      this.chart = echarts.getInstanceByDom(document.getElementById('ringChart'))
      if (this.chart === undefined || this.chart === null) {
        this.chart = echarts.init(document.getElementById('ringChart'))
      }
      this.chart.setOption({
        title: {
          show: true,
          text: this.train_name + '-训练完成情况',
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
        series: [{
          name: '圆环图系列名称', // 系列名称
          type: 'pie', // 系列类型
          center: ['50%', '50%'], // 饼图的中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标。[ default: ['50%', '50%'] ]
          radius: ['40%', '70%'], // 饼图的半径，数组的第一项是内半径，第二项是外半径。[ default: [0, '75%'] ]
          hoverAnimation: true, // 是否开启 hover 在扇区上的放大动画效果。[ default: true ]
          label: { // 饼图图形上的文本标签，可用于说明图形的一些数据信息，比如值，名称等.
            normal: {
              show: false, // 是否显示标签[ default: false ]
              position: 'outside'
            }
          },
          data: this.pieData// 系列中的数据内容数组。
        }],
        // 对图例组件的相关配置
        legend: {
          show: true, // 是否显示
          left: 'center',
          bottom: '2%', // bottom:"20%" // 组件离容器的距离
          itemHeight: 13, // 图例标记的图形高度。
          itemWidth: 13, //  图例标记的图形宽度。
          itemGap: 35, // 图例每项之间的间隔
          icon: 'circle',
          data: ['已完成', '未完成'],
          formatter: (params) => { // 格式化数据的函数
            for (let a = 0; a < this.pieData.length; a++) { // this.pieData  这个数据中有名称和次数
              if (this.pieData[a].name === params) { // 两个名称进行对比，取出对应的次数
                return params + '   ' + this.pieData[a].value + '个' // 然后return你需要的legend格式即可
              }
            }
          },
          textStyle: {
            rich: { // 自定富文本样式
              a: {
                color: '#B6B6B6',
                verticalAlign: 'top',
                align: 'center',
                fontSize: 12,
                padding: [0, 0, 28, 0]
              },
              b: {
                align: 'left',
                fontSize: 18,
                padding: [0, 10, 10, 0],
                lineHeight: 25,
                color: '#181818'
              }
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
