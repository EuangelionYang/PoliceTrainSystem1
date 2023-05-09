<template>
  <div v-loading="loading" class="app-container">
    <el-row :gutter="20">
      <el-col :span="6" :xs="24">
        <el-card class="personal-info">
          <div class="user-avatars">
            <img v-if="userForm.avatar" :src="userForm.avatar">
            <img v-else src="https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png">
          </div>
          <ul class="info-list">
            <li class="list-group-item">
              <div class="list-group-item-p">
                <svg-icon icon-class="user" />
                <span>用户名</span>
                <span class="pull-right">{{ userForm.username || '-' }}</span>
              </div>
            </li>
            <li class="list-group-item">
              <div class="list-group-item-p">
                <svg-icon icon-class="people" />
                <span>姓名</span>
                <span class="pull-right">{{ userForm.name || '-' }}</span>
              </div>
            </li>
            <li class="list-group-item">
              <div class="list-group-item-p">
                <svg-icon icon-class="eye-open" style="cursor:pointer" @click="show = !show" />
                <span>身份证号</span>
                <span v-if="show" class="pull-right">{{ userForm.IDCard || '-' }}</span>
                <span v-else class="pull-right">**********</span>
              </div>
            </li>
            <li class="list-group-item">
              <div class="list-group-item-p">
                <svg-icon icon-class="tree" />
                <span>部门</span>
                <span class="pull-right">{{ userForm.dept_name || '-' }}</span>
              </div>
            </li>
            <li class="list-group-item">
              <div class="list-group-item-p">
                <svg-icon icon-class="post" />
                <span>岗位</span>
                <span class="pull-right">{{ userForm.post_name || '-' }}</span>
              </div>
            </li>
            <li class="list-group-item">
              <div class="list-group-item-p">
                <svg-icon icon-class="lock" />
                <span>角色</span>
                <span class="pull-right">{{ userForm.role_list.toString() || '-' }}</span>
              </div>
            </li>
          </ul>
        </el-card>
      </el-col>
      <el-col :span="18" :xs="24">
        <el-card class="modify-info">
          <el-tabs v-model="activeName">
            <el-tab-pane label="账号修改" name="userinfo">
              <div>
                <p class="info-title"><svg-icon icon-class="phone" />手机号码</p>
                <div class="info-detail">
                  <p>{{ userForm.phone || '暂无' }}</p>
                  <el-button @click="phoneVisible = true">立即修改</el-button>
                </div>
              </div>
              <div>
                <p class="info-title"><svg-icon icon-class="email" />用户邮箱</p>
                <div class="info-detail">
                  <p>{{ userForm.email || '暂无' }}</p>
                  <el-button @click="emailVisible = true">立即修改</el-button>
                </div>
              </div>
              <div>
                <p class="info-title"><svg-icon icon-class="password" />用户密码</p>
                <div class="info-detail">
                  <p>修改用户密码</p>
                  <el-button @click="pwdVisible = true">立即修改</el-button>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog :visible="pwdVisible" title="修改密码" width="400px" @close="handlePwdCancel()">
      <el-form ref="pwdForm" :model="pwdForm" :rules="pwdRules" label-width="80px">
        <el-form-item label="旧密码" prop="oldPassword">
          <el-input v-model="pwdForm.oldPassword" placeholder="请输入旧密码" type="password" />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="pwdForm.newPassword" placeholder="请输入新密码" type="password" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="pwdForm.confirmPassword" placeholder="请确认密码" type="password" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" @click="handleCommitNewPwd()">确定</el-button>
        <el-button @click="handlePwdCancel()">取消</el-button>
      </div>
    </el-dialog>
    <el-dialog :visible="phoneVisible" title="修改手机号码" width="400px" @close="handlePhoneCancel()">
      <p class="dialog-info">您当前的手机号码为：{{ userForm.phone }}</p>
      <el-form ref="phoneForm" :model="phoneForm" :rules="phoneRules" label-width="80px">
        <el-form-item label="手机号码" prop="phone">
          <el-input v-model="phoneForm.phone" placeholder="请输入新的手机号码" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" @click="handleCommitPhone()">确定</el-button>
        <el-button @click="handlePhoneCancel()">取消</el-button>
      </div>
    </el-dialog>
    <el-dialog :visible="emailVisible" title="修改用户邮箱" width="400px" @close="handleEmailCancel()">
      <p class="dialog-info">您当前的邮箱为：{{ userForm.email }}</p>
      <el-form ref="emailForm" :model="emailForm" :rules="emailRules" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="emailForm.email" placeholder="请输入新的邮箱地址" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" @click="handleCommitEmail()">确定</el-button>
        <el-button @click="handleEmailCancel()">取消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { updatePassword, getUniqueUser, updateUserPartial } from '@/api/system/user'
import { mapGetters } from 'vuex'
export default {
  name: 'UserInfo',
  data() {
    const equalToPassword = (rule, value, callback) => {
      if (this.pwdForm.newPassword !== value) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    return {
      loading: true,
      show: false,
      pwdVisible: false,
      phoneVisible: false,
      emailVisible: false,
      activeName: 'userinfo',
      userForm: {
        username: '',
        mobile: '',
        email: '',
        gender: -1,
        dept: {
          deptName: ''
        },
        postName: '',
        role_list: []
      },
      pwdForm: {
        oldPassword: undefined,
        newPassword: undefined,
        confirmPassword: undefined
      },
      phoneForm: {
        phone: ''
      },
      emailForm: {
        email: ''
      },
      emailRules: {
        email: [
          { required: true, message: '邮箱地址不能为空', trigger: 'blur' },
          { type: 'email', message: "'请输入正确的邮箱地址", trigger: ['blur', 'change'] }
        ]
      },
      phoneRules: {
        phone: [
          { required: true, message: '手机号码不能为空', trigger: 'blur' },
          { pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      },
      pwdRules: {
        oldPassword: [{ required: true, message: '旧密码不能为空', trigger: 'blur' }],
        newPassword: [
          { required: true, message: '新密码不能为空', trigger: 'blur' },
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '确认密码不能为空', trigger: 'blur' },
          { required: true, validator: equalToPassword, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters(['name', 'roles', 'avatar', 'id']),
    gender() {
      if (this.userForm.gender === 0) { return '女' } else if (this.userForm.gender === 1) { return '男' }
      return ''
    }
  },
  created() {
    this.getData()
  },
  methods: {
    getData() {
      this.loading = true
      getUniqueUser(this.id).then((res) => {
        this.userForm = res
      }).finally(() => {
        this.loading = false
      })
    },
    handleCommitNewPwd() {
      this.$refs['pwdForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else {
          const params = {
            old_pwd: this.pwdForm.oldPassword,
            new_pwd: this.pwdForm.newPassword
          }
          updatePassword(params).then(() => {
            this.$message.success('修改成功')
          }).finally(() => {
            this.handlePwdCancel()
          })
        }
      })
    },
    handleCommitPhone() {
      this.$refs['phoneForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else {
          const params = new FormData()
          params.append('phone', this.phoneForm.phone)
          updateUserPartial(this.id, params).then(() => {
            this.$message.success('修改成功')
          }).finally(() => {
            this.handlePhoneCancel()
            this.getData()
          })
        }
      })
    },
    handleCommitEmail() {
      this.$refs['emailForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else {
          const params = new FormData()
          params.append('email', this.emailForm.email)
          updateUserPartial(this.id, params).then(() => {
            this.$message.success('修改成功')
          }).finally(() => {
            this.handleEmailCancel()
            this.getData()
          })
        }
      })
    },
    handlePwdCancel() {
      this.pwdVisible = false
      this.$refs.pwdForm.resetFields()
    },
    handlePhoneCancel() {
      this.phoneVisible = false
      this.$refs.phoneForm.resetFields()
    },
    handleEmailCancel() {
      this.emailVisible = false
      this.$refs.emailForm.resetFields()
    }
  }
}
</script>

<style lang="scss" scoped>
.el-card{
  min-height: 520px;
}
.user-avatars {
  //margin: 0 auto;
  overflow: hidden;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  img {
    width: 120px;
    height: 120px;
    object-fit: cover;
  }
}
.info-list {
  padding: 0px;
  list-style: none;
  font-family: "Microsoft YaHei";
  font-size: 14px;
}
.list-group-item{
  line-height: 46px;
}
.list-group-item-p{
  margin-top: 0;
  margin-bottom: 1em;
}
.svg-icon{
  margin-right: 10px;
  font-size: 18px;
}
//.list-group-item {
//  border-bottom: 1px solid #e7eaec;
//  border-top: 1px solid #e7eaec;
//  margin-bottom: -1px;
//  padding: 11px 0px;
//  font-size: 13px;
//}
.pull-right {
  float: right !important;
}
.info-title{
  background-color: #eee;
  line-height: 35px;
  border-radius: 3px;
  padding-left: 30px;
}
.info-detail{
  display: flex;
  justify-content: space-between;
  margin: 0px 30px;
  height: 40px;
}
.dialog-info{
  margin: 0 20px 20px;
}
</style>
