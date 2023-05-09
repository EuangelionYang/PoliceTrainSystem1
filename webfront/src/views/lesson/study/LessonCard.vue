<template>
  <div class="lesson-card-container">
    <el-card :body-style="{ padding: '0px' } " shadow="hover">
      <img v-if="lesson.is_review" :src="lesson.cover" class="item-image" @click="gotoDetail(lesson.id)">
      <img v-else :src="lesson.cover" class="item-image-false">
      <div class="item-body">
        <div>
          <div v-if="lesson.is_review" class="item-title" @click="gotoDetail(lesson.id)">{{ lesson.TrainingName }}</div>
          <div v-else class="item-title-false">{{ lesson.TrainingName }}</div>
        </div>
        <div class="item-desc">{{ lesson.detail || '暂无简介' }}</div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'LessonCard',
  props: {
    lesson: {
      type: Object,
      default: Object
    }
  },
  data() {
    return {}
  },
  mounted() {
  },
  methods: {
    gotoDetail(id) {
      this.$router.push({ path: 'studyDetail', query: { id: id }})
    }
  }
}
</script>

<style lang="scss" scoped>
.lesson-card-container{
  .item-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
  }
  .item-image-false {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
  }
  .item-image:hover {
    cursor: pointer;
  }
  .item-body {
    padding: 20px 12px 10px;
  }
  .item-title {
    font-size: 16px;
    margin-bottom: 12px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #333333;
    font-weight: 500;
  }
  .item-title-false {
    font-size: 16px;
    margin-bottom: 12px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #333333;
    font-weight: 500;
  }
  .item-title:hover {
    cursor: pointer;
    color: #409EFF;
  }
  .item-desc {
    min-height: 20px;
    color: #666;
    font-size: 12px;
    margin-bottom: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

</style>

