<template>
  <div class="app-container">
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          :disabled="permission.add"
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          :disabled="permission.delete"
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          @click="handleDelete"
        >删除</el-button>
      </el-col>
    </el-row>
    <el-table v-loading="loading" :data="roleList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="角色编号" prop="id" width="120" />
      <el-table-column :show-overflow-tooltip="true" label="角色名称" prop="title" />
      <el-table-column :show-overflow-tooltip="true" label="角色编码" prop="identifier" />
      <el-table-column label="状态" prop="status" align="center" width="100">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.status"
            :disabled="permission.update"
            @change="handleStatusChange(scope.row)"
          />
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="scope">
          <el-button
            :disabled="permission.update"
            size="mini"
            type="primary"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
          >修改</el-button>
          <el-button
            :disabled="permission.delete"
            size="mini"
            type="danger"
            icon="el-icon-delete"
            @click="handleDeleteOne(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 添加或修改角色配置对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body @close="dialogCancel()">
      <el-form ref="dialogForm" :model="dialogForm" :rules="rules" label-width="80px">
        <el-form-item label="角色名称" prop="title">
          <el-input v-model="dialogForm.title" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="dialogForm.status">
            <el-radio
              v-for="dict in statusOptions"
              :key="dict.dictValue"
              :label="dict.dictValue"
            >{{ dict.dictLabel }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="角色编码" prop="identifier">
          <el-input v-model="dialogForm.identifier" placeholder="请输入角色编码" />
        </el-form-item>
        <el-form-item label="菜单权限" prop="selectedList">
          <el-checkbox v-model="menuExpand" @change="handleCheckedTreeExpand($event, 'menu')">展开/折叠</el-checkbox>
          <el-checkbox v-model="menuNodeAll" @change="handleCheckedTreeNodeAll($event, 'menu')">全选/全不选</el-checkbox>
          <el-tree
            ref="menu"
            v-model="dialogForm.selectedList"
            :data="menuOptions"
            :props="defaultProps"
            class="tree-border"
            show-checkbox
            node-key="id"
            empty-text="加载中，请稍后"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogSubmit()">确 定</el-button>
        <el-button @click="dialogCancel()">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listRole, changeRoleStatus, getRole, addRole, updateRole, deleteRole, deleteRoleOne, getPermissionTree } from '@/api/system/role'
import { mapGetters } from 'vuex'

export default {
  name: 'Role',
  data() {
    return {
      ids: [],
      loading: false,
      title: '',
      roleList: [],
      editID: -1,
      open: false,
      // 是否显示菜单权限
      menuExpand: false,
      menuNodeAll: false,
      // 状态数据字典
      statusOptions: [
        { dictLabel: '正常', dictValue: true },
        { dictLabel: '停用', dictValue: false }
      ],
      // 菜单列表
      menuOptions: [],
      // 表单参数
      dialogForm: {
        title: '',
        identifier: ''
      },
      defaultProps: {
        children: 'children',
        label: 'title',
        value: 'id'
      },
      permission: {
        add: true,
        delete: true,
        update: true
      },
      // 表单校验
      rules: {
        title: [{ required: true, message: '角色名称不能为空', trigger: 'blur' }],
        status: [{ required: true, message: '角色状态不能为空', trigger: 'blur' }],
        identifier: [{ required: true, message: '角色编码不能为空', trigger: 'blur' }]
      }
    }
  },
  computed: {
    ...mapGetters(['tempBtn', 'menuBtn', 'menuID'])
  },
  created() {
    this.$store.commit('permission/SET_MENUID', 3)
    this.$store.dispatch('permission/getPagePermission', { menu: this.menuBtn, menuid: this.menuID })
    this.getPermission()
    this.getList()
    this.getTree()
  },
  methods: {
    // 查询角色列表
    getList() {
      this.loading = true
      listRole({ no_page: 1 }).then(res => {
        this.roleList = res
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
    getTree() {
      getPermissionTree().then(res => {
        this.menuOptions = this.getTreePermission(res.menu_list)
      })
    },
    getTreePermission(res) {
      for (const ele in res) {
        if (res[ele].children.length !== 0) {
          res[ele].id = 'm' + res[ele].id
          this.getTreePermission(res[ele].children)
        } else {
          res[ele].id = 'm' + res[ele].id
          res[ele].children = res[ele].button_list
          res[ele].children.forEach(e => {
            e.id = 'b' + e.id
          })
        }
      }
      return res
    },
    // 添加角色
    handleAdd() {
      this.title = '添加角色'
      this.open = true
    },
    // 修改角色
    handleUpdate(row) {
      this.editID = row.id
      this.open = true
      this.title = '修改角色'
      getRole(row.id).then(res => {
        this.dialogForm = res
        this.dialogForm.title = res.title
        this.dialogForm.status = res.status
        this.dialogForm.selectedList = []
        if (res.menus) {
          res.menus.forEach(ele => {
            if (ele !== 1 && ele !== 6 && ele !== 12) {
              this.dialogForm.selectedList.push('m' + ele)
            }
          })
        }
        if (res.permissions) {
          res.permissions.forEach(ele => {
            this.dialogForm.selectedList.push('b' + ele)
          })
        }
        this.$refs.menu.setCheckedKeys(this.dialogForm.selectedList)
      })
    },
    // 角色状态修改
    handleStatusChange(row) {
      const text = row.status === true ? '启用' : '停用'
      this.$confirm('确认要' + text + '"' + row.title + '"角色吗?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        changeRoleStatus(row.id, { status: row.status }).then(() => {
          this.$message.success(text + '成功')
        })
      }).finally(() => {
        this.getList()
      })
    },
    handleDelete() {
      if (this.ids.length === 0) {
        this.$message.error('请先勾选待删除角色')
      } else {
        this.$confirm('确定删除所选角色？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteRole({ keys: this.ids }).then(() => {
            this.$message.success('删除成功')
          }).finally(() => {
            setTimeout(() => {
              this.getList()
            }, 100)
          })
        })
      }
    },
    // 删除角色操作
    handleDeleteOne(row) {
      const roleIds = row.id
      this.$confirm('是否确认删除角色编号为"' + roleIds + '"的数据项？删除后绑定该角色的用户的角色将为空', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteRoleOne(row.id).then(() => {
          this.$message.success('删除成功')
        }).finally(() => {
          this.getList()
        })
      })
    },
    handleSelectionChange(selection) {
      this.ids = selection.map((item) => item.id)
    },
    filterIDs() {
      const selectList = this.$refs.menu.getCheckedKeys()
      this.dialogForm.menusPermission = []
      this.dialogForm.btnPermissions = []
      selectList.forEach(ele => {
        if (ele[0] === 'm') {
          this.dialogForm.menusPermission.push(Number(ele.slice(1)))
        } else if (ele[0] === 'b') {
          this.dialogForm.btnPermissions.push(Number(ele.slice(1)))
        }
      })
      this.dialogForm.menusPermission.forEach(ele => {
        if (ele === 2 || ele === 3 || ele === 4 || ele === 5) {
          // 系统管理
          this.dialogForm.menusPermission.push(Number(1))
        } else if (ele === 7 || ele === 8 || ele === 9 || ele === 10 || ele === 11 || ele === 14 || ele === 15) {
          // 训练管理
          this.dialogForm.menusPermission.push(Number(6))
        } else if (ele === 13 || ele === 16) {
          // 统计分析
          this.dialogForm.menusPermission.push(Number(12))
        }
      })
    },
    // 提交按钮
    dialogSubmit() {
      this.$refs['dialogForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else {
          if (this.title === '修改角色') {
            this.filterIDs()
            const params = {
              title: this.dialogForm.title,
              status: this.dialogForm.status,
              menus: this.dialogForm.menusPermission,
              permissions: this.dialogForm.btnPermissions,
              identifier: this.dialogForm.identifier
            }
            updateRole(this.editID, params).then(response => {
              this.$message.success('修改成功')
            }).finally(() => {
              this.dialogCancel()
              this.getList()
            })
          } else if (this.title === '添加角色') {
            this.filterIDs()
            const params = {
              title: this.dialogForm.title,
              status: this.dialogForm.status,
              menus: this.dialogForm.menusPermission,
              permissions: this.dialogForm.btnPermissions,
              identifier: this.dialogForm.identifier
            }
            addRole(params).then(response => {
              this.$message.success('新增成功')
            }).finally(() => {
              this.dialogCancel()
              this.getList()
            })
          }
        }
      })
    },
    // 树权限（展开/折叠）
    handleCheckedTreeExpand(value) {
      const treeList = this.menuOptions
      for (let i = 0; i < treeList.length; i++) {
        this.$refs.menu.store.nodesMap[treeList[i].id].expanded = value
      }
    },
    // 树权限（全选/全不选）
    handleCheckedTreeNodeAll(value) {
      this.$refs.menu.setCheckedNodes(value ? this.menuOptions : [])
    },
    // 取消按钮
    dialogCancel() {
      this.$refs.menu.setCheckedNodes([])
      this.open = false
      this.menuExpand = false
      this.menuNodeAll = false
      this.handleCheckedTreeExpand(this.menuNodeAll)
      this.$refs.dialogForm.resetFields()
    }
  }
}
</script>

<style scoped>

</style>
