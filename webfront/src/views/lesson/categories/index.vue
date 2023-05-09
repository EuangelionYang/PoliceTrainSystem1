<template>
  <div class="app-container category-container">
    <!--    卡片视图-->
    <el-card>
      <el-row :gutter="10" class="mb8">
        <el-col :span="1.5">
          <el-button :disabled="permission.add" type="primary" plain icon="el-icon-plus" size="mini"
                     @click="handleAdd()">新增
          </el-button>
        </el-col>
        <el-col :span="1.5">
          <el-button :disabled="permission.delete" type="danger" plain icon="el-icon-delete" size="mini"
                     @click="handleDelete()">删除
          </el-button>
        </el-col>
      </el-row>
      <!--    表单数据-->
      <el-table v-loading="loading" :ref="categoryList" :data="categoryList" style="padding-top: 20px"
                @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="50" align="center" min-width="10"/>
        <el-table-column label="分类编号" align="center" prop="id"/>
        <!-- <el-table-column label="分类编码" align="center" prop="postCode" /> -->
        <el-table-column label="分类名称" align="center" prop="title"/>
        <el-table-column label="分类排序" align="center" prop="sort"/>
        <el-table-column label="分类类型" align="center" prop="type"/>
        <!-- <el-table-column label="状态" align="center" prop="status" /> -->
        <el-table-column label="创建时间" align="center" prop="created_time">
          <template slot-scope="scope">
            {{ scope.row.created_time.substring(0, 10) + ' ' + scope.row.created_time.substring(11, 19) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="300">
          <template slot-scope="scope">
            <el-button :disabled="permission.update" size="mini" type="primary" icon="el-icon-edit"
                       @click="handleUpdate(scope.row)">修改
            </el-button>
            <el-button :disabled="permission.delete" size="mini" type="danger" icon="el-icon-delete"
                       @click="handleDeleteOne(scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
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
    </el-card>
    <!--    添加分类的对话框-->
    <el-dialog :title="dialogTitle" :visible="dialogVisible" width="350px" @close="handleCancel()">
      <el-form ref="dialogForm" :model="dialogForm" :rules="rules" label-width="80px">
        <el-form-item label="分类名称" prop="title">
          <el-input v-model="dialogForm.title" placeholder="请输入分类名称"/>
        </el-form-item>
        <el-form-item label="分类类型" prop="type">
          <el-select v-model="dialogForm.type" placeholder="请选择动作分类">
            <!-- <template slot="prepend">动作</template> -->
            <el-option label="课程分类" value="课程分类"/>
            <el-option label="情绪课程分类" value="情绪课程分类"/>
            <el-option label="动作课程分类" value="动作课程分类"/>
            <el-option label="心理课程分类" value="心理课程分类"/>
          </el-select>
        </el-form-item>
        <el-form-item label="分类排序" prop="sort">
          <el-input-number v-model="dialogForm.sort" :min="1" :max="10" controls-position="right"/>
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
import {
  getCatagoryList,
  getCatagory,
  addCatagory,
  updateCatagory,
  deleteOneCatagory,
  deleteCatagory
} from '@/api/lesson/catagory'

export default {
  data() {
    return {
      loading: false,
      ids: [],
      selected: false,
      total: 10,
      page: 1,
      limit: 10,
      dialogTitle: '',
      categoryList: [],
      edit_id: -1,
      dialogVisible: false,
      permission: {
        add: false,
        delete: false,
        update: false
      },
      dialogForm: {
        title: '',
        sort: '',
        type: ''
      },
      rules: {
        title: [{required: true, message: '分类名称不能为空', trigger: 'blur'}],
        sort: [{required: true, message: '分类排序不能为空', trigger: 'blur'}],
        type: [{required: true, message: '分类类型不能为空', trigger: 'blur'}]
      }
    }
  },
  created() {
    this.getData()
  },
  methods: {
    getData() {
      this.loading = true
      const params = {
        page: this.page,
        limit: this.limit
      }
      getCatagoryList(params).then(res => {
        this.categoryList = res.data
        this.total = res.total
      }).finally(() => {
        this.loading = false
      })
    },
    handleSelectionChange(selection) {
      this.ids = selection.map((item) => item.id)
      this.selected = !selection.length
    },
    handleCancel() {
      this.dialogVisible = false
      this.$refs.dialogForm.resetFields()
    },
    handleCommit() {
      this.$refs['dialogForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else {
          if (this.dialogTitle === '添加分类') {
            const params = {
              title: this.dialogForm.title,
              sort: this.dialogForm.sort,
              type: this.dialogForm.type
            }
            addCatagory(params).then(() => {
              this.$message.success('添加成功')
            }).finally(() => {
              setTimeout(() => {
                this.getData()
              }, 500)
            })
          } else if (this.dialogTitle === '修改分类') {
            const params = {
              title: this.dialogForm.title,
              sort: this.dialogForm.sort,
              type: this.dialogForm.type
            }
            updateCatagory(this.edit_id, params).then(() => {
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
    handleUpdate(row) {
      this.dialogTitle = '修改分类'
      this.dialogVisible = true
      this.edit_id = row.id
      getCatagory(row.id).then(res => {
        this.dialogForm = res
      })
    },
    handleAdd() {
      this.dialogTitle = '添加分类'
      this.dialogVisible = true
    },
    handleDeleteOne(row) {
      this.$confirm('确认要删除' + row.title + '分类吗？', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteOneCatagory(row.id).then(() => {
          this.$message.success('删除成功')
        }).finally(() => {
          setTimeout(() => {
            this.page = 1
            this.getData()
          }, 500)
        })
      })
    },
    handleDelete() {
      if (this.ids.length === 0) {
        this.$message.error('请先勾选待删除分类')
      } else {
        this.$confirm('确认要删除所选分类吗？', '警告', {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteCatagory({keys: this.ids}).then(res => {
            this.$message.success('删除成功')
          }).finally(() => {
            setTimeout(() => {
              this.page = 1
              this.getData()
            }, 500)
          })
        })
      }
    },
    handleSizeChange(limit) {
      this.limit = limit
      this.page = 1
      this.getData()
    },
    handleCurrentChange(page) {
      this.page = page
      this.getData()
    }
  }
}
</script>

<style lang='scss' scoped>
.category-container {
  .page_area {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
}
</style>
