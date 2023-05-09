<template>
  <!--  这个是教务能看到的页面  -->
  <div class="app-container lesson-list-container">
    <!--增删按钮-->
    <div v-if="role" class="manage-container">
      <el-row :gutter="10">
        <el-col :span="1.5">
          <el-button
            type="primary"
            plain
            icon="el-icon-plus"
            size="mini"
            @click="addLesson()"
          >添加
          </el-button>
        </el-col>
        <el-col :span="1.5">
          <el-button
            type="danger"
            plain
            icon="el-icon-delete"
            size="mini"
            @click="deleteLesson()"
          >删除
          </el-button>
        </el-col>
      </el-row>
    </div>
    <!--    训练列表区域-->
    <el-table v-loading="loading" :data="lessonList" style="width: 100%" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="id" label="序号" width="50" align="center" />
      <el-table-column prop="TrainingName" align="center" label="训练名称" />
      <el-table-column prop="TrainingID" align="center" label="训练编号" />
<!--      <el-table-column prop="category" align="center" label="训练类型" />-->
      con
      <el-table-column prop="is_publish" align="center" label="发布状态" width="100">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.is_publish" type="success">已发布</el-tag>
          <el-tag v-else type="danger">未发布</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_review" align="center" label="审核状态" width="100">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.is_review" type="success">已审核</el-tag>
          <el-tag v-else type="danger">未审核</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="learner_number" align="center" label="学员人数" width="100" />
      <el-table-column prop="teacher_name" align="center" label="教官" width="100" />
      <el-table-column prop="create_time" align="center" label="添加时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_time.substring(0, 10) + ' ' + scope.row.create_time.substring(11, 19) }}
        </template>
      </el-table-column>
      <el-table-column v-if="!role" label="操作" width="200" align="center">
        <template slot-scope="scope">
          <el-button type="warning" size="mini" icon="el-icon-edit" @click="handleCourse(scope.row)">编辑</el-button>
          <el-button type="primary" size="mini" icon="el-icon-view" @click="checkCourse(scope.row)">查看</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="role" label="审核操作" width="200" align="center">
        <template slot-scope="scope">
          <el-button type="warning" icon="el-icon-edit" size="mini" @click="updateLesson(scope.row)">修改</el-button>
          <el-button type="primary" size="mini" icon="el-icon-s-check" @click="checkCourse(scope.row)">审核</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--  添加或修改参数配置对话框  -->
    <el-dialog :title="title" :visible="openDialog" width="800px" custom-class="training-dialog" @close="cancel">
      <el-form v-loading="dialogLoading" ref="dialogForm" :model="dialogForm" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="训练名称" prop="TrainingName">
              <el-input v-model="dialogForm.TrainingName" clearable placeholder="请输入训练名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="训练分类" prop="TrainingCate">
              <el-select v-model="dialogForm.category" style="width: 300px" clearable filterable placeholder="请选择训练分类">
                <el-option v-for="item in categoryOptions" :key="item.id" :label="item.title" :value="item.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="教官" prop="teacher">
              <el-select v-model="dialogForm.teacher" style="width: 300px" clearable filterable placeholder="请选择教官">
                <el-option v-for="item in teacherOptions" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="训练编码" prop="TrainingID">
              <el-input v-model="dialogForm.TrainingID" style="width: 300px" clearable placeholder="请输入训练编码" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="训练简介" prop="detail">
              <el-input resize="none" v-model="dialogForm.detail" :rows="3" type="textarea" maxlength="250" show-word-limit placeholder=" 示例：从基础到搭建项目视频课程。专业名称注意大小写" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="课程封面" prop="cover">
          <upload-avatar
            v-model="cover_cache"
            :image-url="cover_cache"
            :width="150"
            :height="150"
            @getAvatarFile="getAvatarFile"
          />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" @click="onSubmit()">提 交</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
    <el-pagination
      v-if="total > 0"
      :current-page="page"
      :total="total"
      :page-sizes="[5, 10, 20, 50]"
      :page-size="limit"
      class="page_area"
      background
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script>
import { getTrainingListByTeacher, getTrainingListByEducation, getTeachers, getOneTraining, addTraining, updateTraining, deleteTraining } from '@/api/lesson/lessonList'
import { getCatagoryList } from '@/api/lesson/catagory'
import { mapGetters } from 'vuex'
import uploadAvatar from '@/components/Avatar/uploadAvatar.vue'

export default {
  name: 'LessonList',
  components: {
    uploadAvatar
  },
  data() {
    return {
      loading: false,
      dialogLoading: false,
      // 删除时表格未选中禁用
      selected: true,
      // dialog标题
      title: '',
      // 选中数组
      ids: [],
      // 添加修改训练表单弹出框
      openDialog: false,
      total: 0, // 总记录条数
      page: 1, // 当前页码
      limit: 10, // 每页显示的记录个数
      cover_cache: '',
      is_cover_update: false,
      // 训练列表
      lessonList: [],
      // 表单参数
      dialogForm: {
        TrainingName: '',
        TrainingID: '',
        learners: [],
        teacher: '',
        cover: '',
        detail: '',
        category: ''
      },
      // 表单校验
      rules: {
        TrainingName: [{ required: true, message: '训练名称不能为空', trigger: 'blur' }],
        TrainingID: [{ required: true, message: '训练编码不能为空', trigger: 'blur' }],
        category: [{ required: true, message: '训练分类不能为空', trigger: 'change' }],
        learners: [{ required: true, message: '学员不能为空', trigger: 'change' }],
        teacher: [{ required: true, message: '教官不能为空', trigger: 'change' }],
        cover: [{ required: true, message: '封面图片不能为空', trigger: 'blur' }],
        detail: [{ required: true, message: '简介不能为空', trigger: 'blur' }]
      },
      // 教官选择器
      teacherOptions: [],
      categoryOptions: [],
      role: null,
      // 上传课程封面列表
      fileList: [],
      // 学员列表
      userList: []
    }
  },
  computed: {
    ...mapGetters(['roles', 'identifier', 'id'])
  },
  created() {
    this.identifier.forEach(ele => {
      if (ele === 'education') {
        this.role = true
      } else if (ele === 'teacher') {
        this.role = false
      }
    })
    this.getCourseList()
    this.getTeacherList()
    this.getCategory()
  },
  methods: {
    // 获取训练列表
    getCourseList() {
      this.loading = true
      if (this.role === true) {
        const params = {
          page: this.page,
          limit: this.limit
        }
        getTrainingListByEducation(params).then(res => {
          this.lessonList = res.data
          this.total = res.total
        }).finally(() => {
          this.loading = false
        })
      } else {
        const params = {
          page: this.page,
          limit: this.limit,
          teacher_id: this.id
        }
        getTrainingListByTeacher(params).then(res => {
          this.lessonList = res.data
          this.total = res.total
        }).finally(() => {
          this.loading = false
        })
      }
    },
    getTeacherList() {
      getTeachers().then(res => {
        this.teacherOptions = res
      })
    },
    getCategory() {
      getCatagoryList({ no_page: 1 , type: '课程分类'}).then(res => {
        this.categoryOptions = res
      })
    },
    // 新增训练
    addLesson() {
      this.openDialog = true
      this.title = '添加训练'
    },
    // 提交表单按钮
    onSubmit() {
      this.$refs['dialogForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else {
          if (this.title === '添加训练') {
            const params = new FormData()
            params.append('TrainingID', this.dialogForm.TrainingID)
            params.append('TrainingName', this.dialogForm.TrainingName)
            params.append('TrainingCate', this.dialogForm.TrainingCate)
            params.append('teacher', this.dialogForm.teacher)
            params.append('cover', this.dialogForm.cover)
            params.append('detail', this.dialogForm.detail)
            params.append('category', this.dialogForm.category)
            console.log(params.get('category'))
            addTraining(params).then(res => {
              this.$message.success('添加成功')
            }).finally(() => {
              setTimeout(() => {
                this.getCourseList()
              }, 500)
            })
          } else if (this.title === '修改训练详情') {
            const params = new FormData()
            params.append('TrainingID', this.dialogForm.TrainingID)
            params.append('TrainingName', this.dialogForm.TrainingName)
            params.append('TrainingCate', this.dialogForm.TrainingCate)
            params.append('teacher', this.dialogForm.teacher)
            params.append('detail', this.dialogForm.detail)
            params.append('category', this.dialogForm.category)
            if (this.is_cover_update) {
              params.append('cover', this.dialogForm.cover)
            }
            updateTraining(this.dialogForm.id, params).then(res => {
              this.$message.success('修改成功')
            }).finally(() => {
              setTimeout(() => {
                this.getCourseList()
              }, 500)
            })
          }
          this.cancel()
        }
      })
    },
    // 取消按钮
    cancel() {
      this.openDialog = false
      this.$refs.dialogForm.resetFields()
      this.cover_cache = ''
    },
    // 编辑课程信息
    handleCourse(row) {
      if (row.is_publish) {
        this.$message.error('该训练已发布，不能进行编辑！')
        return
      } else {
        this.$router.push({ path: 'upload', query: { id: row.id }})
      }
    },
    // 删除训练
    deleteLesson(row) {
      if (this.ids.length === 0) {
        this.$message.error('请先勾选待删除训练')
      } else {
        this.$confirm('确定删除所选训练？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteTraining({ keys: this.ids }).then(() => {
            this.$message.success('删除成功')
          }).finally(() => {
            this.getCourseList()
          })
        })
      }
    },
    // 修改训练详情
    updateLesson(row) {
      if (row.is_publish) {
        this.$message.error('该训练已发布，不能进行修改')
        return
      } else {
        this.dialogLoading = true
        this.openDialog = true
        this.title = '修改训练详情'
        getOneTraining(row.id).then(res => {
          this.dialogForm = res
          console.log(this.dialogForm)
          this.cover_cache = this.dialogForm.cover
          if (this.cover_cache === null) {
            this.cover_cache = ''
          }
          if (this.dialogForm.category === null) {
            this.dialogForm.category = ''
          }
        }).finally(() => {
          this.dialogLoading = false
        })
        this.is_cover_update = false
      }
    },
    // 审核已发布的训练
    checkCourse(row) {
      if (row.is_publish === false) {
        this.$message.error('该训练未发布，不能进行查看/审核')
        return
      } else {
        this.$router.push({ path: 'check', query: { id: row.id }})
      }
    },
    getAvatarFile(data) {
      // 如果子组件调用了这个方法的话，说明头像被修改了，需要上传，否则就不用上传
      this.is_cover_update = true
      // 这里好像有个问题，用双向绑定的话，把cover传过来会出错，是一个文件类型，而不是url地址。
      this.dialogForm.cover = data
      this.cover_cache = URL.createObjectURL(this.dialogForm.cover)
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.selected = !selection.length
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
.lesson-list-container {
  .page_area {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
}
</style>
<style lang="scss">
.training-dialog {
  .el-input__count {
    top: 75px;
    right: 25px;
    line-height: 15px;
  }

  .el-transfer-panel {
    width: 300px;
  }

  .el-transfer__buttons {
    width: 80px;
    padding: 10px;

    .el-transfer__button {
      margin: 10px 0px;
    }
  }
}
</style>
