<template>
  <div class="chapterList">
    <el-menu
      :default-active="chapterList.index"
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
    >
      <el-submenu v-for="(chap,index) in chapterList" :key="chap.id" :index="chap.id+''">
        <template slot="title">
          <span>视频{{ index + 1 }} {{ chap.chapterTitle }}</span>
        </template>
        <el-menu-item :index="chap.chapterTitle" @click="handleClick(chap)">
          <span class="svg-container" style="padding-right: 8px">
            <svg-icon v-if="chap.is_finish" icon-class="finish" />
            <svg-icon v-else icon-class="unfinish" />
          </span>
          {{ chap.chapterTitle }}
        </el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'ChapterList',
  props: {
    chapterList: {
      type: Array,
      default: Array
    }
  },
  data() {
    return {}
  },
  mounted() {},
  methods: {
    handleOpen() {
      // console.log('open')
    },
    handleClose() {
      // console.log('close')
    },
    handleClick(chap) {
      this.$emit('getWhichVideo', chap.chapterFile)
      // this.$bus.$emit('playMovie', { url: url })
    }
  }
}
</script>

<style lang="scss" scoped>
.el-menu-item{
  overflow: hidden;
  text-overflow:ellipsis ;
}
</style>
