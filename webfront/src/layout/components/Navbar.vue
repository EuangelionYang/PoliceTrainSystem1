<template>
  <div class="navbar">
    <hamburger :is-active="sidebar.opened" class="hamburger-container" @toggleClick="toggleSideBar"/>

    <breadcrumb class="breadcrumb-container"/>

    <div class="right-menu">
      <el-dropdown class="avatar-container" trigger="click" @command="handleCommand">
        <div class="avatar-wrapper">
          <span class="user-name">{{ name }}</span>
          <el-avatar :src="avatar" class="user-avatar" @error="handleError()">
            <img src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png">
          </el-avatar>
          <!-- <img src="avatar" class="user-avatar"> -->
          <i class="el-icon-caret-bottom"/>
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">

          <!--          <router-link to="/userInfo">-->
          <el-dropdown-item :disabled="tag" command="info">
            个人中心
          </el-dropdown-item>
          <!--          </router-link>-->
          <!--          <a target="_blank" href="https://github.com/PanJiaChen/vue-admin-template/">-->
          <!--            <el-dropdown-item>Github</el-dropdown-item>-->
          <!--          </a>-->

          <el-dropdown-item divided @click.native="handleLogout">
            <span style="display: block">退出系统</span>
          </el-dropdown-item>

        </el-dropdown-menu>

      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'

export default {
  components: {
    Breadcrumb,
    Hamburger
  },
  data() {
    return {
      tag: false
    }
  },
  computed: {
    ...mapGetters(['sidebar', 'name', 'avatar', 'token', 'roles', 'permission_routes', 'identifier'])
  },
  created() {
    // console.log(this.identifier.indexOf('admin'))
    if (this.identifier.indexOf('admin') > -1) {
      this.tag = true
    }
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    handleError() {
      return true
    },
    handleLogout() {
      this.$confirm('确定要退出系统吗', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.logout()
      })
    },
    async logout() {
      await this.$store.dispatch('user/logout')
      location.reload()
      this.$router.replace('/login')
    },
    handleCommand(command) {
      if (command === 'info') {
        this.$router.push('/userInfo')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background 0.3s;
    -webkit-tap-highlight-color: transparent;

    &:hover {
      background: rgba(0, 0, 0, 0.025);
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background 0.3s;

        &:hover {
          background: rgba(0, 0, 0, 0.025);
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;
        padding-right: 2px;

        .user-name {
          margin-right: 9px;
          font-size: 16px;
        }

        .user-avatar {
          cursor: pointer;
          width: 30px;
          height: 30px;
          border-radius: 50%;
          margin-top: 5px;
          margin-bottom: 0px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}
</style>
<style lang="scss">
.navbar {
  .avatar-container {
    .user-avatar {
      img {
        width: 100% !important;
        height: auto !important;
      }
    }
  }
}
</style>
