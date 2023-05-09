<template>
  <div class="post-container app-container">
    <!--    搜索框-->
    <!-- <el-form ref="queryForm" :model="queryParams" :inline="true" label-width="68px">
      <el-form-item label="岗位编码" prop="postCode">
        <el-input
          v-model="queryParams.postCode"
          placeholder="请输入岗位编码"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="岗位名称" prop="postName">
        <el-input
          v-model="queryParams.postName"
          placeholder="请输入岗位名称"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="岗位状态" clearable size="small">
          <el-option label="正常" value="1" />
          <el-option label="停用" value="0" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="getData()">搜索</el-button>
      </el-form-item>
    </el-form> -->
    <!--    功能按钮-->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button :disabled="permission.add" type="primary" plain icon="el-icon-plus" size="mini" @click="handleAdd()">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button :disabled="permission.delete" type="danger" plain icon="el-icon-delete" size="mini" @click="handleDelete()">删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="warning" plain icon="el-icon-download" size="mini" @click="handleExport()">导出</el-button>
      </el-col>
    </el-row>
    <!--    表单数据-->
    <el-table v-loading="loading" :ref="postList" :data="postList" style="padding-top: 20px" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="岗位编号" align="center" prop="id" />
      <!-- <el-table-column label="岗位编码" align="center" prop="postCode" /> -->
      <el-table-column label="岗位名称" align="center" prop="title" />
      <el-table-column label="岗位排序" align="center" prop="sort" />
      <!-- <el-table-column label="状态" align="center" prop="status" /> -->
      <el-table-column label="创建时间" align="center" prop="create_time" width="180" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button :disabled="permission.update" size="mini" type="primary" icon="el-icon-edit" @click="handleUpdate(scope.row)">修改</el-button>
          <el-button :disabled="permission.delete" size="mini" type="danger" icon="el-icon-delete" @click="handleDeleteOne(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogTitle" :visible="dialogVisible" width="350px" @close="handleCancel()">
      <el-form ref="dialogForm" :model="dialogForm" :rules="rules" label-width="80px">
        <el-form-item label="岗位名称" prop="title">
          <el-input v-model="dialogForm.title" placeholder="请输入岗位名称" />
        </el-form-item>
        <el-form-item label="岗位排序" prop="sort">
          <el-input-number v-model="dialogForm.sort" :min="1" :max="10" controls-position="right" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" @click="handleCommit()">提交</el-button>
        <el-button type="primary" @click="handleCancel()">取消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getPostList, getOnePost, addPost, updatePost, deletePostOne, deletePost } from '@/api/system/post'
import { mapGetters } from 'vuex'

export default {
  name: 'Post',
  data() {
    return {
      loading: true,
      ids: [],
      selected: false,
      dialogTitle: '',
      dialogForm: {
        title: '',
        sort: 0
      },
      editId: -1,
      dialogVisible: false,
      multipleSelection: '',
      excelData: '',
      permission: {
        add: true,
        delete: true,
        update: true
      },
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        postCode: undefined,
        postName: undefined,
        status: undefined
      },
      // statusOptions: [
      //   { dictLabel: '正常', dictValue: true },
      //   { dictLabel: '停用', dictValue: false }
      // ],
      // 表单参数
      postList: [],
      rules: {
        title: [{ required: true, message: '岗位名称不能为空', trigger: 'blur' }],
        sort: [{ required: true, message: '岗位排序不能为空', trigger: 'blur' }]
      }
    }
  },
  computed: {
    ...mapGetters(['tempBtn', 'menuBtn', 'menuID'])
  },
  created() {
    this.$store.commit('permission/SET_MENUID', 5)
    this.$store.dispatch('permission/getPagePermission', { menu: this.menuBtn, menuid: this.menuID })
    this.getPermission()
    this.getData()
  },
  methods: {
    getData() {
      this.loading = true
      getPostList({ noPage: 1 }).then(res => {
        this.postList = res.data
      }).finally(() => {
        this.loading = false
      })
    },
    getPermission() {
      this.tempBtn.forEach(ele => {
        if (ele.title === '新增') {
          this.permission.add = false
        } else if (ele.title === '删除') {
          this.permission.delete = false
        } else if (ele.title === '更新') {
          this.permission.update = false
        }
      })
    },
    handleQuery() {
      this.queryParams.pageNum = 1
      this.getPostList()
    },
    handleSelectionChange(selection) {
      this.multipleSelection = selection
      this.ids = selection.map((item) => item.id)
      this.selected = !selection.length
    },
    handleAdd() {
      this.dialogTitle = '新增岗位'
      this.dialogVisible = true
    },
    handleUpdate(row) {
      this.dialogTitle = '修改岗位'
      this.dialogVisible = true
      this.editId = row.id
      getOnePost(row.id).then(res => {
        this.dialogForm.title = res.title
        this.dialogForm.sort = res.sort
      })
    },
    handleCommit() {
      this.$refs['dialogForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else {
          if (this.dialogTitle === '新增岗位') {
            const params = {
              title: this.dialogForm.title,
              sort: this.dialogForm.sort
            }
            addPost(params).then(() => {
              this.$message.success('添加成功')
            }).finally(() => {
              setTimeout(() => {
                this.getData()
              }, 500)
            })
          } else if (this.dialogTitle === '修改岗位') {
            const params = {
              title: this.dialogForm.title,
              sort: this.dialogForm.sort
            }
            updatePost(this.editId, params).then(() => {
              this.$message.success('修改成功')
            }).finally(() => {
              setTimeout(() => {
                this.getData()
              }, 500)
            })
          }
          this.handleCancel()
        }
      })
    },
    handleCancel() {
      this.dialogVisible = false
      this.$refs.dialogForm.resetFields()
    },
    handleDeleteOne(row) {
      this.$confirm('确认要删除' + row.title + '岗位吗？', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deletePostOne(row.id).then(() => {
          this.$message.success('删除成功')
        }).finally(() => {
          setTimeout(() => {
            this.getData()
          }, 500)
          this.getData()
        })
      })
    },
    handleDelete() {
      if (this.ids.length === 0) {
        this.$message.error('请先勾选待删除岗位')
      } else {
        this.$confirm('确认要删除所选岗位吗？', '警告', {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deletePost({ keys: this.ids }).then(res => {
            this.$message.success('删除成功')
          }).finally(() => {
            setTimeout(() => {
              this.getData()
            }, 500)
          })
        })
      }
    },
    handleExport() {
      if (this.multipleSelection.length === 0) {
        this.$message.success('暂无数据可导出')
        return
      }
      this.$confirm('确定下载列表文件?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.excelData = this.multipleSelection // multipleSelection是一个数组，存储表格中选择的行的数据。
        this.export2Excel()
        this.$message.success('请关注浏览器中的下载')
      })
    },
    export2Excel() {
      var that = this
      require.ensure([], () => {
        const {
          export_json_to_excel
        } = require('@/excel/export2Excel') // 这里必须使用绝对路径，使用@/+存放export2Excel的路径
        const tHeader = ['岗位编号', '岗位名称', '岗位排序', '创建时间'] // 导出的表头名信息
        const filterVal = ['id', 'title', 'sort', 'create_time'] // 导出的表头字段名，需要导出表格字段名
        const list = that.excelData
        const data = that.formatJson(filterVal, list)
        export_json_to_excel(tHeader, data, '岗位列表') // 导出的表格名称
      })
    },
    // 格式转换
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
    }
  }
}
</script>

<style lang="scss">
.post-container{
  .el-input-number{
    width: 100%;
  }
}
</style>
