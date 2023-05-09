<template>
  <div class="user_info_container">
    <el-card>
      <el-row :gutter="20">
        <el-col>
          <!-- 搜索框 -->
          <el-form
            ref="queryForm"
            :model="queryParams"
            :inline="true"
            label-width="68px"
          >
            <el-form-item label="搜索" prop="name">
              <el-input
                v-model="queryParams.search"
                placeholder="请输入姓名/账号"
                clearable
                size="small"
                style="width: 240px"
                @keyup.enter.native="getList('search')"
                @input="getList('search')"
                @clear="getList()"
              />
            </el-form-item>
            <el-form-item label="状态" prop="is_active">
              <!--数据库中状态一栏应是0或者1，这样才能根据:value修改状态栏-->
              <el-select
                v-model="queryParams.is_active"
                placeholder="请选择"
                clearable
                size="small"
                style="width: 240px"
                @clear="getList()"
                @change="getList('search')"
              >
                <el-option :value="1" label="正常" />
                <el-option :value="0" label="停用" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" icon="el-icon-search" size="mini" class="search-btn" @click="getList('search')()">搜索
              </el-button>
            </el-form-item>
          </el-form>
          <!--增删导入导出按钮-->
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button :disabled="permission.add" type="primary" plain icon="el-icon-plus" size="mini" @click="handleAdd()">新增</el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button :disabled="permission.delete" type="danger" plain icon="el-icon-delete" size="mini" @click="handleDelete()">删除</el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button type="info" plain icon="el-icon-upload2" size="mini" @click="handleImport()">导入</el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button type="warning" plain icon="el-icon-download" size="mini" @click="handleExport()">导出</el-button>
            </el-col>
          </el-row>
          <!--用户列表区域-->
          <el-table
            v-loading="loading"
            :data="userList"
            style="width: 100%"
            @sort-change="sortChange"
            @selection-change="handleSelectionChange"
          >
            <el-table-column :selectable="selectEnable" type="selection" width="50" align="center" fixed="left" />
            <el-table-column sortable="id" width="80" label="编号" align="center" prop="id" />
            <el-table-column :show-overflow-tooltip="true" label="用户账号" align="center" prop="username" />
            <el-table-column :show-overflow-tooltip="true" label="姓名" align="center" prop="name">
              <template slot-scope="scope">
                <span>{{ scope.row.name || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column :show-overflow-tooltip="true" prop="gender" label="性别" width="50" align="center" />
            <el-table-column :show-overflow-tooltip="true" label="身份证号" width="200" align="center">
              <template slot-scope="scope">
                <span v-if="!scope.row.show">
                  <span class="idcard">**************************</span>
                  <svg-icon icon-class="eye" class="eye" @click="scope.row.show = true" />
                </span>
                <span v-else>
                  <span class="idcard">{{ scope.row.IDCard || '-' }}</span>
                  <svg-icon icon-class="eye-open" class="eye" @click="scope.row.show = false" />
                </span>
              </template>
            </el-table-column>
            <el-table-column key="role" :show-overflow-tooltip="true" label="角色" align="center">
              <template slot-scope="scope">
                <template v-if="scope.row.role_list.length > 0">
                  <span v-for="item in scope.row.role_list" :key="item">{{ item + ' ' }}</span>
                </template>
                <template v-else><span>-</span></template>
              </template>
            </el-table-column>
            <el-table-column key="is_active" width="80" label="状态" align="center">
              <template slot-scope="scope">
                <el-switch v-model="scope.row.is_active" :disabled="permission.update" @change="handleStatusChange(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column label="手机号" align="center" prop="phone" width="160">
              <template slot-scope="scope">
                <span>{{ scope.row.phone || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center" width="180" fixed="right" class-name="small-padding fixed-width">
              <template slot-scope="scope">
                <el-tooltip :enterable="false" effect="light" content="修改信息" placement="bottom">
                  <el-button :disabled="permission.update" size="mini" type="primary" icon="el-icon-edit" @click="handleUpdate(scope.row)" />
                </el-tooltip>
                <el-tooltip :enterable="false" effect="light" content="重置密码" placement="bottom">
                  <el-button :disabled="permission.update" size="mini" type="warning" icon="el-icon-key" @click="handleResetPwd(scope.row)" />
                </el-tooltip>
                <el-tooltip :enterable="false" effect="light" content="人脸照片" placement="bottom">
                  <el-button size="mini" type="info" icon="el-icon-camera" @click="handleShowFace(scope.row.id)" />
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column label="更多" align="center" width="80" fixed="right" class-name="small-padding fixed-width">
              <template slot-scope="scope">
                <el-button :disabled="moreEnable(scope.row)" size="mini" icon="el-icon-more" @click="handleMore(scope.row)" />
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
        </el-col>
      </el-row>
    </el-card>
    <!--  添加或修改参数配置对话框  -->
    <el-dialog :title="title" :visible="open" width="600px" @close="handleCancel()">
      <el-form ref="dialogForm" :model="dialogForm" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="dialogForm.name" placeholder="请输入用户昵称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色" prop="role">
              <el-select v-model="dialogForm.role" multiple placeholder="请选择" collapse-tags>
                <el-option
                  v-for="item in roleOptions"
                  :key="item.id"
                  :label="item.title"
                  :value="item.id"
                  :disabled="item.status == 0"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="dialogForm.phone" placeholder="请输入手机号码" maxlength="11" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="dialogForm.email" placeholder="请输入邮箱" maxlength="50" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="身份证号" prop="IDCard">
              <el-input v-model="dialogForm.IDCard" placeholder="请输入身份证号" maxlength="18" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="部门" prop="dept">
              <el-cascader
                v-model="dialogForm.dept"
                :options="deptOptions"
                :props="listProps"
                :show-all-levels="false"
                placeholder="请选择用户所在部门"
                clearable
              />
              <!-- <el-select v-model="dialogForm.dept" placeholder="请选择用户所在部门">
                <el-option v-for="item in deptOptions" :key="item.id" :label="item.title" :value="item.id" />
              </el-select> -->
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="岗位" prop="post">
              <el-select v-model="dialogForm.post" placeholder="请选择用户岗位">
                <el-option v-for="item in postOptions" :key="item.id" :label="item.title" :value="item.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item v-if="!is_edit" label="用户账号" prop="username">
              <el-input v-model="dialogForm.username" placeholder="请输入用户账号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item v-if="!is_edit" label="用户密码" prop="password">
              <el-input v-model="dialogForm.password" placeholder="请输入用户密码" type="password" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="dialogForm.gender" placeholder="请选择">
                <el-option v-for="item in sexOptions" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="is_active">
              <el-radio-group v-model="dialogForm.is_active">
                <el-radio v-for="dict in statusOptions" :key="dict.dictValue" :label="dict.dictValue">
                  {{ dict.dictLabel }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户头像" prop="avatar">
              <upload-avatar
                v-model="avatar_cache"
                :image-url="avatar_cache"
                :width="width"
                :height="height"
                @getAvatarFile="getAvatarFile"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="其他信息" prop="detail">
              <el-upload
                ref="upload"
                :file-list="detailFile"
                :limit="1"
                :on-remove="handleDetailRemove"
                :http-request="detailHttpRequest"
                :on-exceed="handleDetailExceed"
                :show-file-list="true"
                action="#"
              >
                <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
              </el-upload>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleCommit()">确 定</el-button>
        <el-button @click="handleCancel()">取 消</el-button>
      </div>
    </el-dialog>
    <el-dialog :visible="picVisible" title="用户人脸照片" width="820px" @close="handleFaceCancel()">
      <div v-loading="faceLoading" class="dialog-add-pic">
        <p>此处展示用户人脸照片，该照片将用于该用户进行人脸识别登录！</p>
        <el-upload
          ref="cardUpload"
          :disabled="permission.update"
          :limit="4"
          :file-list="faceUrlList"
          :http-request="faceHttpRequest"
          :on-exceed="handleFaceExceed"
          :before-upload="beforeFaceUpload"
          accept="image/pjpeg, image/jpeg, image/jpg, image/png, image/x-png"
          action="#"
          list-type="picture-card"
          multiple
        >
          <i slot="default" class="el-icon-plus" />
          <div slot="file" slot-scope="{file}">
            <img :src="file.url" class="el-upload-list__item-thumbnail" alt="">
            <span class="el-upload-list__item-actions">
              <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                <i class="el-icon-zoom-in" />
              </span>
              <span v-if="!permission.update" class="el-upload-list__item-delete" @click="handleFaceRemove(file)">
                <i class="el-icon-delete" />
              </span>
            </span>
          </div>
        </el-upload>
        <span v-if="permission.update" slot="tip"> 您无权限进行上传操作！</span>
        <div slot="footer" class="dialog-pic-footer">
          <el-button type="primary" @click="handleFaceCancel()">确定</el-button>
        </div>
      </div>
    </el-dialog>
    <el-dialog :visible="showPicVisible" title="照片查看" width="500px" @close="closePicDialog">
      <img :src="dialogImageUrl" width="100%" alt="">
    </el-dialog>
    <el-dialog :visible="importVisible" title="导入数据" width="300px" @close="closeImport">
      <el-button type="primary" class="down-import-model" @click="downImportModel()">下载导入数据模板</el-button>
      <el-upload
        :http-request="importRequest"
        :limit="1"
        :auto-upload="true"
        action="#"
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"
      >
        <el-button type="primary">导入已填写好的数据</el-button>
        <div slot="tip" class="el-upload__tip">只 能 上 传 xlsx / xls 文 件</div>
      </el-upload>
      <!-- <div slot="footer">
        <el-button type="primary">确定</el-button>
      </div> -->
    </el-dialog>

  </div>
</template>

<script>
import { listUser, addUser, updateUser, deleteUser, getRoleList, getUniqueUser, resetPassword, updateUserPartial } from '@/api/system/user'
import { getUserFace, addUserFace, deleteUserFace, userExport, userImport } from '@/api/system/user'
import { getPostList } from '@/api/system/post'
import { getDeptList } from '@/api/system/dept'
import uploadAvatar from '@/components/Avatar/uploadAvatar.vue'
import { mapGetters } from 'vuex'
import axios from 'axios'

export default {
  name: 'User',
  components: {
    uploadAvatar
  },
  data() {
    return {
      baseURL: '',
      avatar_cache: '',
      sort: '',
      show: false,
      ids: [],
      total: 0,
      userList: null,
      loading: false,
      faceLoading: true,
      title: '',
      open: false, // 添加/修改用户对话框显隐
      importVisible: false,
      showPicVisible: false,
      dialogImageUrl: '',
      is_edit: false,
      is_detail_update: false,
      is_avatar_update: false,
      edit_id: -1,
      picVisible: false,
      faceList: [],
      faceUrlList: [],
      width: 100,
      height: 100,
      detailFile: [],
      showFaceid: -1,
      multipleSelection: '',
      excelData: '',
      permission: {
        add: true,
        delete: true,
        update: true
      },
      // 状态数据字典
      statusOptions: [
        { dictLabel: '正常', dictValue: true },
        { dictLabel: '停用', dictValue: false }
      ],
      sexOptions: [
        { id: 1, name: '男' },
        { id: 0, name: '女' }
      ],
      roleOptions: [],
      deptOptions: [],
      postOptions: [],
      listProps: {
        value: 'id',
        label: 'title',
        children: 'children',
        checkStrictly: true
      },
      // 表单参数
      dialogForm: {
        username: '',
        name: '',
        gender: 1,
        is_active: true,
        role: [],
        avatar: '',
        phone: '',
        email: '',
        detail: '',
        password: '',
        IDCard: '',
        dept: null,
        post: null,
        show: false
      },
      page: 1,
      limit: 10,
      // 查询参数
      queryParams: {
        search: '',
        is_active: undefined
      },
      // 表单校验
      rules: {
        username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
        name: [{ required: true, message: '姓名不能为空', trigger: 'blur' }],
        password: [{ required: true, message: '用户密码需至少6位', trigger: 'blur' }],
        email: [{ type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }],
        phone: [{ pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/, message: '请输入正确的手机号码', trigger: 'blur' }],
        gender: [{ required: true, message: '性别不能为空', trigger: 'blur' }],
        is_active: [{ required: true, message: '状态不能为空', trigger: 'blur' }],
        role: [{ required: true, message: '用户角色不能为空', trigger: 'change' }],
        IDCard: [{ required: true, pattern: /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/, message: '请输入正确的用户身份证号', trigger: 'blur' }],
        dept: [{ required: true, message: '用户部门不能为空', trigger: 'change' }],
        post: [{ required: true, message: '用户岗位不能为空', trigger: 'change' }]
      }
    }
  },
  computed: {
    ...mapGetters(['tempBtn', 'menuBtn', 'menuID'])
  },
  watch: {
    sort(newValue, oldValue) {
      this.page = 1
      this.getList()
    }
  },
  created() {
    this.$store.commit('permission/SET_MENUID', 2)
    this.$store.dispatch('permission/getPagePermission', { menu: this.menuBtn, menuid: this.menuID })
    this.getPermission()
    this.getRoleOptions()
    this.getDeptOptions()
    this.getPostOptions()
    this.getList()
  },
  methods: {
    change(row) {
      row.show = !row.show
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
    getList(arc) {
      this.userList = []
      this.total = 0
      this.loading = true
      if (arc === 'search') {
        this.page = 1
      }
      const params = {
        page: this.page,
        limit: this.limit,
        ordering: this.sort,
        search: this.queryParams.search,
        is_active: this.queryParams.is_active
      }
      listUser(params).then((res) => {
        res.data.forEach(ele => {
          ele.show = false
          if (ele.gender === 0) {
            ele.gender = '女'
          } else if (ele.gender === 1) {
            ele.gender = '男'
          }
        })
        this.userList = res.data
        this.total = res.total
      }).finally(() => {
        this.loading = false
      })
    },
    getRoleOptions() {
      getRoleList({ no_page: 1 }).then(res => {
        this.roleOptions = res
      })
    },
    getDeptOptions() {
      getDeptList().then(res => {
        this.deptOptions = this.listBFS(res)
      })
    },
    getPostOptions() {
      getPostList({ no_page: 1 }).then(res => {
        this.postOptions = res
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
    selectEnable(row) {
      return !row.is_admin
    },
    moreEnable(row) {
      return !row.detail
    },
    handleSelectionChange(selection) {
      this.multipleSelection = selection
      this.ids = selection.map((item) => item.id)
    },
    handleResetPwd(row) {
      this.$confirm('确认要重置用户' + row.username + '的密码吗?  注意：密码将被重置为123456', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const params = {
          id: row.id,
          new_pwd: '123456'
        }
        resetPassword(params).then(() => {
          this.$message.success('用户' + row.name + '密码重置成功，已重置为123456')
        })
      })
    },
    handleStatusChange(row) {
      const text = row.is_active === true ? '启用' : '停用'
      this.$confirm('确认要' + text + row.username + '用户吗?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const params = new FormData()
        params.append('is_active', row.is_active)
        updateUserPartial(row.id, params).then(() => {
          this.$message.success(text + '成功')
        })
      }).finally(() => {
        setTimeout(() => {
          this.getList()
        }, 500)
      })
    },
    handleAdd() {
      this.open = true
      this.title = '添加用户'
      this.is_edit = false
    },
    handleDetailRemove(file, fileList) {
      this.dialogForm.detail = ''
      this.detailFile = []
      this.is_detail_update = true
    },
    detailHttpRequest(option) {
      this.is_detail_update = true
      const file = option.file
      this.detailFile.push(file)
      this.dialogForm.detail = this.detailFile[0]
    },
    handleDetailExceed() {
      this.$message.error('最多支持1个附件上传！')
    },
    handleShowFace(id) {
      this.showFaceid = id
      this.picVisible = true
      this.getFace()
    },
    getFace() {
      this.faceLoading = true
      this.faceList = []
      this.faceUrlList = []
      getUserFace({ uid: this.showFaceid }).then(res => {
        this.faceList = res
        this.faceList.forEach(ele => {
          this.faceUrlList.push({
            name: ele.id,
            url: ele.face
          })
        })
      }).finally(() => {
        this.faceLoading = false
      })
    },
    handleFaceCancel() {
      this.picVisible = false
      this.faceList = []
      this.faceUrlList = []
    },
    handleFaceRemove(file, fileList) {
      let deletePic = -1
      this.faceList.forEach(ele => {
        if (ele.face === file.url) {
          deletePic = ele.id
        }
      })
      deleteUserFace(deletePic).then(res => {
        this.$message.success('删除成功')
      }).finally(() => {
        this.getFace()
      })
    },
    faceHttpRequest(option) {
      const file = option.file
      const params = new FormData()
      params.append('uid', this.showFaceid)
      params.append('face', file)
      this.faceLoading = true
      this.faceList = []
      this.faceUrlList = []
      addUserFace(params).then(() => {
        this.$message.success('添加成功')
      }).finally(() => {
        this.getFace()
      })
    },
    handleFaceExceed() {
      this.$message.error('最多支持4张照片上传！')
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url
      this.showPicVisible = true
    },
    closePicDialog() {
      this.showPicVisible = false
      this.dialogImageUrl = ''
    },
    beforeFaceUpload(file) {
      const imageType = ['image/pjpeg', 'image/jpeg', 'image/jpg', 'image/png', 'image/x-png']
      const isJPG = imageType.indexOf(file.type) > -1
      const isLt2M = file.size / 1024 / 1024 < 5
      if (!isJPG) {
        this.$message.error('上传头像图片只能是图片格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 5MB!')
      }
      return isJPG && isLt2M
    },
    // 点击修改用户信息后，获取用户的全部信息
    handleUpdate(row) {
      this.open = true
      this.title = '修改用户'
      this.is_edit = true
      getUniqueUser(row.id).then(res => {
        this.dialogForm = res
        // 这里存一下avatar，因为从后端返回过来的avatar是一个url
        // 但是如果更新头像的话，dialogForm里的avatar得是文件类型才可以。
        this.avatar_cache = this.dialogForm.avatar
        if (this.avatar_cache === null) {
          this.avatar_cache = ''
        }
        this.edit_id = row.id
        const ele = this.dialogForm.detail
        if (ele) {
          const obj = {}
          const index = ele.lastIndexOf('\/')
          const fileName = ele.substring(index + 1, ele.length)
          obj['name'] = fileName
          obj['url'] = ele
          this.detailFile.push(obj)
        }
      })
      this.is_detail_update = false
      this.is_avatar_update = false
    },
    handleUserUpdate() {
      const params = new FormData()
      params.append('name', this.dialogForm.name)
      params.append('gender', this.dialogForm.gender)
      params.append('is_active', this.dialogForm.is_active)
      params.append('phone', this.dialogForm.phone)
      params.append('email', this.dialogForm.email)
      params.append('IDCard', this.dialogForm.IDCard)
      params.append('dept', this.dialogForm.dept instanceof Array ? this.dialogForm.dept[this.dialogForm.dept.length - 1] : this.dialogForm.dept)
      params.append('post', this.dialogForm.post)
      this.dialogForm.role.forEach(ele => {
        params.append('role', ele)
      })
      if (this.dialogForm.avatar === null) {
        params.append('avatar', '')
      } else if (this.is_avatar_update) {
        params.append('avatar', this.dialogForm.avatar)
      }
      if (this.dialogForm.detail === null) {
        params.append('detail', '')
      } else if (this.is_detail_update) {
        params.append('detail', this.dialogForm.detail)
      }
      updateUser(this.edit_id, params).then((res) => {
        if (res.status === 200) {
          this.$message.success('修改成功')
        }
      }).catch(() => {
        this.$message.warning('修改失败')
      })
    },
    handleUserAdd() {
      const params = new FormData()
      params.append('username', this.dialogForm.username)
      params.append('name', this.dialogForm.name)
      params.append('gender', this.dialogForm.gender)
      params.append('is_active', this.dialogForm.is_active)
      params.append('phone', this.dialogForm.phone)
      params.append('email', this.dialogForm.email)
      params.append('password', this.dialogForm.password)
      this.dialogForm.role.forEach(ele => {
        params.append('role', ele)
      })
      params.append('avatar', this.dialogForm.avatar)
      params.append('detail', this.dialogForm.detail)
      params.append('IDCard', this.dialogForm.IDCard)
      params.append('dept', this.dialogForm.dept instanceof Array ? this.dialogForm.dept[this.dialogForm.dept.length - 1] : this.dialogForm.dept)
      params.append('post', this.dialogForm.post)
      addUser(params).then((res) => {
        if (res.status === 200) {
          this.$message.success('添加成功')
        }
      }).catch(() => {
        this.$message.warning('添加失败')
      }).finally(() => {
        this.getList()
      })
    },
    getAvatarFile(data) {
      // 如果子组件调用了这个方法的话，说明头像被修改了，需要上传，否则就不用上传
      this.is_avatar_update = true
      // 这里好像有个问题，用双向绑定的话，把avatar传过来会出错，是一个文件类型，而不是url地址。
      this.dialogForm.avatar = data
      this.avatar_cache = URL.createObjectURL(this.dialogForm.avatar)
    },
    handleCommit() {
      this.$refs['dialogForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else {
          if (this.is_edit) {
            this.handleUserUpdate()
          } else {
            this.handleUserAdd()
          }
          this.clearDialog()
          setTimeout(() => {
            this.getList()
          }, 100)
          this.open = false
        }
      })
    },
    handleCancel() {
      this.open = false
      this.clearDialog()
      this.detailFile = []
    },
    clearDialog() {
      this.$refs.dialogForm.resetFields()
      this.dialogForm.username = ''
      this.avatar_cache = ''
    },
    handleDelete() {
      if (this.ids.length === 0) {
        this.$message.error('请先勾选待删除用户')
      } else {
        this.$confirm('确定删除所选用户？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteUser({ keys: this.ids }).then(() => {
            this.$message.success('删除成功')
          }).finally(() => {
            setTimeout(() => {
              this.getList()
            }, 100)
          })
        })
      }
    },
    handleMore(row) {
      const a = document.createElement('a')
      a.href = row.detail
      a.click()
    },
    sortChange(column, prop, order) {
      if (column.order === null) {
        this.sort = ''
        return
      }
      switch (column.prop) {
        case 'id':
          if (column.order === 'descending') this.sort = 'id'
          if (column.order === 'ascending') this.sort = '-id'
          break
        default:
          this.sort = ''
      }
    },
    // 用户导出
    handleExport() {
      if (this.multipleSelection.length === 0) {
        this.$confirm('您未勾选数据，将为您导出所有用户数据', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          const params = {
            keys: 'all'
          }
          userExport(params).then(res => {
            res.forEach(ele => {
              if (ele.gender === 0) {
                ele.gender = '女'
              } else if (ele.gender === 1) {
                ele.gender = '男'
              }
            })
            this.excelData = res
            this.export2Excel()
            this.$message.success('请关注浏览器中的下载')
          })
        })
        return
      }
      this.$confirm('确定下载当前页面选中的用户数据列表文件?', '提示', {
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
        const tHeader = ['用户账号', '用户姓名', '用户性别', '身份证号', '用户角色', '状态', '手机号'] // 导出的表头名信息
        const filterVal = ['username', 'name', 'gender', 'IDCard', 'role_list', 'is_active', 'phone'] // 导出的表头字段名，需要导出表格字段名
        const list = that.excelData
        const data = that.formatJson(filterVal, list)
        export_json_to_excel(tHeader, data, '用户列表') // 导出的表格名称
      })
    },
    // 格式转换
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
    },
    // 用户导入
    handleImport() {
      this.importVisible = true
    },
    closeImport() {
      this.importVisible = false
    },
    downImportModel() {
      axios.get('static/user_template.xlsx', {
        responseType: 'blob'
      }).then(res => {
        const url = window.URL.createObjectURL(new Blob([res.data]))
        const link = document.createElement('a')
        const fname = '用户导入模板.xlsx'
        link.href = url
        link.setAttribute('download', fname)
        document.body.appendChild(link)
        link.click()
      }).catch(error => {
        console.log('error:' + JSON.stringify(error))
      })
    },
    importRequest(option) {
      const file = option.file
      const params = new FormData()
      params.append('users_file', file)
      userImport(params).then(() => {
        this.$message.success('添加成功')
        this.importVisible = false
      }).finally(() => {
        this.getList()
      })
    },
    handleSizeChange(limit) {
      this.limit = limit
      this.page = 1
      this.getList()
    },
    handleCurrentChange(page) {
      this.page = page
      this.getList()
    }
  }
}
</script>

<style lang="scss" scoped>
.user_info_container {
  .page_area {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }

  .dialog-pic-footer {
    margin-top: 20px;
  }

  .search-btn {
    margin-left: 20px;
  }
  .down-import-model{
    margin-bottom: 20px;
  }
  .eye{
    cursor: pointer;
    margin-left: 10px;
  }
  .idcard{
    width: 145px;
    display: inline-block;
  }
}
</style>
