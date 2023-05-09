<template>
  <div>
    <el-container>
      <!--      <el-header>-->
      <!--        <div style="font-size: 20px;text-align: center ;margin: 50px">-->
      <!--          {{ name }}，欢迎您，开始您一天的工作吧！-->
      <!--        </div>-->
      <!--      </el-header>-->
      <!--      <el-divider></el-divider>-->
      <el-main>

        <div style="float: right">
          <div style="font-size: 25px;text-align: center ;float: left">
            {{ name }}，欢迎您，开始一天的工作吧！
          </div>
          <el-calendar v-model="date" style="width: 40%;float: right">
          </el-calendar>
        </div>

      </el-main>
    </el-container>


  </div>


</template>

<script>
import {mapGetters} from 'vuex'
import PieChart from '@/views/score/components/PieChart'
import RadarChart from '@/views/score/components/RadarChart'
import RingGauge from '@/views/score/components/RingGauge'

export default {
  name: 'Dashboard',
  components: {PieChart, RingGauge, RadarChart},
  data() {
    return {
      date: new Date()
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'roles',
      'avatar'
    ])
  }
}
</script>

<style lang="scss" scoped>
.main {
  text-align: center;
  background-color: #fff;
  border-radius: 20px;
  width: 300px;
  height: 350px;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

//.dashboard-container {
//  .dashboard-header {
//    padding-top: 100px;
//    padding-left: 100px;
//    padding-right: 400px;
//
//    .dashboard-avatar {
//      display: inline-block;
//
//      .user-avatar {
//        display: inline-block;
//        height: 45px;
//        width: 45px;
//
//        img {
//          width: 100% !important;
//          height: auto !important;
//        }
//      }
//    }
//
//    .title {
//      display: inline-block;
//      padding: 0 0 0 15px;
//      position: relative;
//      top: -15px;
//
//      h1 {
//        font-size: 1.5rem;
//        font-weight: 500;
//        line-height: 1.75rem;
//        margin: 0 auto;
//      }
//
//      span {
//        font-size: 14px;
//        color: rgba(0, 0, 0, .45);
//      }
//    }
//  }
//}
//
//.dashboard {
//  &-text {
//    font-size: 30px;
//    line-height: 46px;
//  }
//}
.dashboard-container {
  .user-avatar {
    display: inline-block;
    height: 45px;
    width: 45px;

    img {
      width: 100% !important;
      height: auto !important;
    }
  }
}

@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
