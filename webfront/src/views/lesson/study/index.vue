<template>
  <div class="app-container lessons-cards-container">
    <div class="pageContainer">
      <!-- 分类栏 -->
      <div class="my-course-box">
        <el-card>
          <div class="marBom" style="padding-top: 10px">
            <div class="titleWrap">
              <span class="classifyTitle">训练类型</span>
            </div>
            <div class="curStyle">
              <span
                v-for="(item,index) in categoryList"
                :key="index"
                :class="{'active': item.isActive}"
                class="category-item"
                @click="searchLesson(item)"
              >{{ item.title }}</span>
            </div>
          </div>
        </el-card>
      </div>
      <!--      搜索框-->
      <div class="search-wrapper" style="margin-top: 30px;padding-left: 20px">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="search"
              placeholder="快速查找"
              clearable
              autocomplete="off"
              @keyup.enter.native="getAllLessons('search')"
              @clear="getAllLessons()"
            />
          </el-col>
          <el-col :span="1.5">
            <el-button type="primary" icon="el-icon-search" @click="getAllLessons('search')">查询</el-button>
          </el-col>
        </el-row>
      </div>
      <div v-loading="loading">
        <!--        <span v-if="total===0" description="请选择章节">haha </span>-->
        <div v-if="total===0" class="empty">
          <div>
            <img :src="emptyImg" alt="暂无数据">
          </div>
          <p style="color:#B0AFAF">暂无数据</p>
        </div>
        <div v-else>
          <!--课程列表-->
          <lesson-list :lessonlist="lessonList"/>
        </div>
      </div>
      <el-pagination
        v-if="total > 0"
        :current-page="page"
        :total="total"
        :page-sizes="[9, 12, 15, 18]"
        :page-size="limit"
        class="page_area"
        background
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>

</template>

<script>
import {getTrainingListByUser} from '@/api/lesson/lessonList'
import {getCatagoryList} from '@/api/lesson/catagory'
import LessonList from '@/views/lesson/study/LessonList'
import {mapGetters} from 'vuex'
import imgUrl from '@/assets/images/empty.svg'

export default {
  name: 'Study',
  components: {LessonList},
  // eslint-disable-next-line vue/no-unused-components
  data() {
    return {
      loading: false,
      total: 0,
      page: 1,
      limit: 9,
      search: '',
      activeName: 'myClass',
      ruleForm: '',
      token: '',
      lessonList: [],
      categoryList: [],
      category: null,
      emptyImg: imgUrl
    }
  },
  computed: {
    ...mapGetters(['id'])
  },
  created() {
    this.getAllLessons()
    this.getAllCategory()
  },
  methods: {
    getAllLessons(arc) {
      this.loading = true
      if (arc === 'search') {
        this.page = 1
      }
      const params = {
        page: this.page,
        limit: this.limit,
        search: this.search,
        category: this.category
      }
      const data = {
        uid: this.id
      }
      getTrainingListByUser(params, data).then(res => {
        this.lessonList = res.data
        this.total = res.total
      }).finally(() => {
        this.loading = false
      })
    },
    getAllCategory() {
      getCatagoryList({no_page: 1, type: '课程分类'}).then(res => {
        res.forEach(ele => {
          ele.isActive = false
        })
        res.unshift({id: -1, title: '全部', isActive: true})
        this.categoryList = res
      })
    },
    searchLesson(item) {
      this.categoryList.forEach(ele => {
        ele.isActive = false
      })
      item.isActive = true
      if (item.id === -1) {
        this.category = null
      } else {
        this.category = item.id
      }
      this.getAllLessons('search')
    },
    handleClick(tab, event) {
      console.log(tab, event)
    },
    getCourseList() {
      this.currentPage = 1
      this.limit = 5
    },
    handleSizeChange(limit) {
      this.limit = limit
      this.page = 1
      this.getCourseList()
    },
    handleCurrentChange(page) {
      this.page = page
      this.getCourseList()
    }
  }
}
</script>

<style lang="scss" scoped>
.lessons-cards-container {
  .pageContainer {
    .page_area {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }

    .my-course-box {
      .marBom {
        margin-bottom: 15px;
        display: flex;
        font-size: 14px;

        .titleWrap {
          width: 75px;
          text-align: center;
          line-height: 38px;

          .classifyTitle {
            color: #333333;
            font-weight: 600;
          }
        }

        .curStyle {
          width: calc(100% - 75px);
          display: flex;
          flex-wrap: wrap;

          .category-item {
            cursor: pointer;
            padding: 5px 10px;
            margin: 5px 10px;
            border: 1px solid #fff;
          }

          .active {
            border: 1px solid #d7eaff;
            background-color: #ecf5ff;
            color: #43a2ff;
            border-radius: 5px;
          }
        }
      }
    }

    .empty {
      text-align: center;
      padding-top: 50px
    }
  }
}
</style>
