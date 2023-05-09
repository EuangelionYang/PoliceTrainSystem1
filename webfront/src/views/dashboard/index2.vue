<template>
  <div class="dashboard-container">
    <!--    <div class="dashboard-text">name: {{ name }}</div>-->
    <!--    <div class="dashboard-text">roles: <span v-for="role in roles" :key="role">{{ role }}</span></div>-->
    <div class="dashboard-header">
      <div class="dashboard-avatar">
        <el-avatar :src="avatar" class="user-avatar">
          <img src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png">
        </el-avatar>
      </div>
      <div class="title">
        <h1>{{ name }}，欢迎您，开始您一天的工作吧！</h1>
      </div>
    </div>
    <div class="dashboard-body">
      <img src="https://wpimg.wallstcn.com/0e03b7da-db9e-4819-ba10-9016ddfdaed3" alt="" class="emptyGif">
      <!-- <el-row :gutter="32">
        <el-col :xs="24" :sm="24" :lg="8">
          <div class="chart-wrapper">
            <radar-chart />
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="8">
          <div class="chart-wrapper">
            <pie-chart />
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="8">
          <div class="chart-wrapper">
            <RingGauge/>
          </div>
        </el-col>
      </el-row> -->
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import PieChart from '@/views/score/components/PieChart'
import RadarChart from '@/views/score/components/RadarChart'
import RingGauge from '@/views/score/components/RingGauge'

export default {
  name: 'Dashboard',
  components: { PieChart, RingGauge, RadarChart },
  data() {
    return {
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
.dashboard-container{
  .dashboard-header{
    padding: 40px;
    .dashboard-avatar{
    display: inline-block;
    .user-avatar{
      display: inline-block;
      height: 45px;
      width: 45px;
      img{
        width: 100% !important;
        height: auto !important;
      }
    }
  }
    .title{
    display: inline-block;
    padding: 0 0 0 15px;
    position: relative;
    top: -5px;
    h1{
      font-size: 1.125rem;
      font-weight: 500;
      line-height: 1.75rem;
    }
    span{
      font-size: 14px;
      color: rgba(0,0,0,.45);
    }
  }
  }
  .dashboard-body{
    padding: 32px;
    background-color: rgb(240, 242, 245);
    position: relative;
    .chart-wrapper {
      background: #fff;
      padding: 16px 16px 0;
      margin-bottom: 32px;
    }
  }
}
.dashboard {
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
<style lang="scss">
.dashboard-container{
  .user-avatar{
    display: inline-block;
    height: 45px;
    width: 45px;
    img{
      width: 100% !important;
      height: auto !important;
    }
  }
}
</style>
