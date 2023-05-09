<template>
  <div class="course-list" style="padding-top: 25px;margin-left:40px;margin-right: -50px">
    <el-row>
      <el-col
        v-for="lessonObj in lessonlist"
        :key="lessonObj.id"
        :span="6"
        :offset="1"
        style="margin-bottom: 25px"
      >
        <LessonCard :key="lessonObj.id" :lesson="lessonObj" />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import LessonCard from '@/views/lesson/study/LessonCard'

export default {
  components: { LessonCard },
  props: {
    lessonlist: {
      type: Array,
      default: Array
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
