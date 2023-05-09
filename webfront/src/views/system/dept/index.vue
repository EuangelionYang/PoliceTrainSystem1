<template>
  <div class="dept-container app-container">
    <div class="dept-header">
      <el-button :disabled="permission.add" type="primary" plain icon="el-icon-plus" size="mini" @click="handleAdd()">新增</el-button>
    </div>
    <el-table
      v-loading="loading"
      :data="deptList"
      :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
      border
      row-key="id"
      default-expand-all
    >
      <el-table-column prop="title" label="部门名称" />
      <el-table-column prop="sort" label="部门排序" />
      <el-table-column prop="leader" label="主管人员">
        <template slot-scope="scope">
          {{ whichLeader(scope.row.leader) }}
        </template>
      </el-table-column>
      <el-table-column prop="telephone" label="部门电话">
        <template slot-scope="scope">
          {{ scope.row.telephone || '-' }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button :disabled="permission.update" size="mini" type="primary" icon="el-icon-edit" @click="handleUpdate(scope.row)">修改</el-button>
          <el-button :disabled="scope.row.parentID === null || permission.delete" size="mini" type="danger" icon="el-icon-delete" @click="handleDeleteOne(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogTitle" :visible="visible" width="500px" @close="dialogClose()">
      <el-form ref="dialogForm" :model="dialogForm" :rules="dialogRules" label-width="80px">
        <el-form-item v-if="dialogTitle === '添加部门'" label="上级部门" prop="parentID">
          <el-cascader v-model="dialogForm.parentID" :options="deptList" :props="listProps" placeholder="请选择上级部门" clearable />
        </el-form-item>
        <el-form-item label="部门名称" prop="title">
          <el-input v-model="dialogForm.title" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="显示排序" prop="sort">
          <el-input-number v-model="dialogForm.sort" :min="0" :max="10" controls-position="right" />
        </el-form-item>
        <el-form-item label="主管人员" prop="leader">
          <el-select v-model="dialogForm.leader" placeholder="请选择主管人员">
            <el-option v-for="item in userList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="部门电话" prop="telephone">
          <el-input v-model="dialogForm.telephone" placeholder="请输入部门电话" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" @click="dialogCommit()">确定</el-button>
        <el-button @click="dialogClose()">取消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getDeptList, addDept, updateDept, deleteDept, getDeptOne } from '@/api/system/dept'
import { listUser } from '@/api/system/user'
import { mapGetters } from 'vuex'

export default {
  name: 'Dept',
  data() {
    return {
      queryParams: {
        deptName: '',
        status: ''
      },
      loading: false,
      dialogTitle: '',
      visible: false,
      dialogForm: {
        title: '',
        parentID: '',
        sort: '',
        leader: '',
        telephone: ''
      },
      permission: {
        add: true,
        delete: true,
        update: true
      },
      statusOptions: [
        { dictLabel: '正常', dictValue: true },
        { dictLabel: '停用', dictValue: false }
      ],
      listProps: {
        value: 'id',
        label: 'title',
        children: 'children',
        checkStrictly: true
      },
      deptList: [],
      userList: [],
      dialogRules: {
        parentID: [{ required: true, message: '上级部门不能为空', trigger: 'change' }],
        title: [{ required: true, message: '部门名称不能为空', trigger: 'blur' }],
        sort: [{ required: true, message: '显示排序不能为空', trigger: 'blur' }],
        leader: [{ required: true, message: '主管人员不能为空', trigger: 'change' }],
        phone: [{ pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/, message: '请输入正确的手机号码', trigger: 'blur' }]
      }
    }
  },
  computed: {
    ...mapGetters(['tempBtn', 'menuBtn', 'menuID'])
  },
  created() {
    this.$store.commit('permission/SET_MENUID', 4)
    this.$store.dispatch('permission/getPagePermission', { menu: this.menuBtn, menuid: this.menuID })
    this.getPermission()
    this.getData()
    this.getUser()
  },
  methods: {
    getUser() {
      listUser({ no_page: 1 }).then(res => {
        this.userList = res
      })
    },
    listBFS(res) {
      for (const ele in res) {
        if (res[ele].children.length !== 0) {
          this.listBFS(res[ele].children)
        } else {
          delete res[ele]['children']
        }
      }
      return res
    },
    getData() {
      this.loading = true
      getDeptList().then(res => {
        this.deptList = this.listBFS(res)
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
    whichLeader(leaderID) {
      let name = '-'
      this.userList.forEach(ele => {
        if (leaderID === ele.id) {
          name = ele.name
        }
      })
      return name
    },
    handleUpdate(row) {
      this.dialogTitle = '修改部门'
      this.edit_id = row.id
      this.visible = true
      getDeptOne(row.id).then(res => {
        this.dialogForm = res
      })
    },
    handleAdd() {
      this.dialogTitle = '添加部门'
      this.visible = true
    },
    handleDeleteOne(row) {
      this.$confirm('确认要删除该部门吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteDept(row.id).then(() => {
          this.$message.success('删除成功')
        }).finally(() => {
          setTimeout(() => {
            this.getData()
          }, 500)
        })
      })
    },
    dialogClose() {
      this.visible = false
      this.$refs.dialogForm.resetFields()
    },
    dialogCommit() {
      this.$refs['dialogForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else {
          if (this.dialogTitle === '修改部门') {
            const params = {
              parentID: this.dialogForm.parentID instanceof Array ? this.dialogForm.parentID[this.dialogForm.parentID.length - 1] : this.dialogForm.parentID,
              title: this.dialogForm.title,
              sort: this.dialogForm.sort,
              leader: this.dialogForm.leader,
              telephone: this.dialogForm.telephone
            }
            updateDept(this.edit_id, params).then(() => {
              this.$message.success('修改成功')
            }).finally(() => {
              setTimeout(() => {
                this.getData()
              }, 500)
            })
          } else if (this.dialogTitle === '添加部门') {
            const params = {
              parentID: this.dialogForm.parentID[this.dialogForm.parentID.length - 1],
              title: this.dialogForm.title,
              sort: this.dialogForm.sort,
              leader: this.dialogForm.leader,
              telephone: this.dialogForm.telephone
            }
            addDept(params).then(() => {
              this.$message.success('添加成功')
            }).finally(() => {
              setTimeout(() => {
                this.getData()
              }, 500)
            })
          }
          this.dialogClose()
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dept-container{
  .dept-header{
    margin-bottom: 20px;
  }
}
</style>
<style lang="scss">
.dept-container{
  .el-input__inner{
    width: 100%;
  }
  .el-cascader{
    width: 100%;
  }
  .el-input-number{
    width: 100%;
  }
  .el-select{
    width: 100%;
  }
}
</style>
