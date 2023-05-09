<template>
  <div class="app-container action-container">
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
      <el-table v-loading="loading" :ref="actionList" :data="actionList" style="padding-top: 20px"
                @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center"/>
        <el-table-column label="动作编号" align="center" prop="id"/>
        <el-table-column label="动作名称" align="center" prop="actionName"/>
        <el-table-column label="动作编码" align="center" prop="identifier"/>
        <el-table-column label="动作分类" align="center" prop="type"/>
        <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
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
    <!--    添加动作的对话框-->
    <el-dialog :title="dialogTitle" :visible="dialogVisible" width="350px" @close="handleCancel()">
      <el-form ref="dialogForm" :model="dialogForm" :rules="rules" label-width="80px">
        <el-form-item label="动作名称" prop="actionName">
          <el-input v-model="dialogForm.actionName" placeholder="请输入动作名称"/>
        </el-form-item>
        <el-form-item label="动作编码" prop="identifier">
          <el-input v-model="dialogForm.identifier" placeholder="请输入动作编码"/>
        </el-form-item>
        <el-form-item label="动作分类" prop="type">
          <el-select v-model="dialogForm.type" placeholder="请选择动作分类">
            <!-- <template slot="prepend">动作</template> -->
            <el-option label="动作" value="动作"/>
            <el-option label="情绪" value="情绪"/>
            <el-option label="语气" value="语气"/>
            <el-option label="关节" value="关节"/>
          </el-select>
          <!--          <el-input v-model="dialogForm.type" placeholder="请输入动作分类"/>-->
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
import {getActionList, getAction, addAction, updateAction, deleteOneAction, deleteAction} from '@/api/lesson/action'

export default {
  data() {
    return {
      typeList: ['动作', '情绪', '语气', '关节'],
      loading: false,
      ids: [],
      selected: false,
      total: 10,
      page: 1,
      limit: 10,
      dialogTitle: '',
      actionList: [],
      edit_id: -1,
      dialogVisible: false,
      permission: {
        add: false,
        delete: false,
        update: false
      },
      dialogForm: {
        actionName: '',
        identifier: '',
        type: ''
      },
      rules: {
        actionName: [{required: true, message: '动作名称不能为空', trigger: 'blur'}],
        identifier: [{required: true, message: '动作编码不能为空', trigger: 'blur'}],
        type: [{required: true, message: '动作分类不能为空', trigger: 'blur'}]
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
      getActionList(params).then(res => {
        this.actionList = res.data
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
          if (this.dialogTitle === '添加动作') {
            const params = {
              actionName: this.dialogForm.actionName,
              identifier: this.dialogForm.identifier,
              type: this.dialogForm.type
            }
            addAction(params).then(() => {
              this.$message.success('添加成功')
            }).finally(() => {
              setTimeout(() => {
                this.getData()
              }, 500)
            })
          } else if (this.dialogTitle === '修改动作') {
            const params = {
              actionName: this.dialogForm.actionName,
              identifier: this.dialogForm.identifier,
              type: this.dialogForm.type
            }
            updateAction(this.edit_id, params).then(() => {
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
      this.dialogTitle = '修改动作'
      this.dialogVisible = true
      this.edit_id = row.id
      getAction(row.id).then(res => {
        this.dialogForm = res
      })
    },
    handleAdd() {
      this.dialogTitle = '添加动作'
      this.dialogVisible = true
    },
    handleDeleteOne(row) {
      this.$confirm('确认要删除' + row.actionName + '动作吗？', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteOneAction(row.id).then(() => {
          this.$message.success('删除成功')
        }).finally(() => {
          setTimeout(() => {
            this.getData()
          }, 500)
        })
      })
    },
    handleDelete() {
      if (this.ids.length === 0) {
        this.$message.error('请先勾选待删除动作')
      } else {
        this.$confirm('确认要删除所选动作吗？', '警告', {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteAction({keys: this.ids}).then(res => {
            this.$message.success('删除成功')
          }).finally(() => {
            setTimeout(() => {
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
.action-container {
  .page_area {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
}
</style>
