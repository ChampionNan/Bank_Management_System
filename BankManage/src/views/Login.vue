<template>
  <div>
    <div class="title">登陆界面</div>
    <el-form ref="form" :model="form" label-width="80px" validate @submit.native.prevent>
      <el-form-item label="登陆类型">
        <el-select v-model="custype" class="dropbtn" placeholder="请选择登陆类型">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item v-if="custype === SUB_BANK" label="支行名称">
        <el-input class="input" id="username" v-model="username" aria-required="true" placeholder="Please input username"></el-input>
      </el-form-item>
      <el-form-item v-else label="身份证号">
        <el-input class="input" id="username" v-model="username" aria-required="true" placeholder="Please input username"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="password" placeholder="Please input your password" aria-required="true" class="input" id="password" show-password></el-input>
      </el-form-item>
      <el-button type="success" @click.native="login" round>登陆</el-button>
      <el-button type="primary" @click.native="register" round>注册</el-button>
    </el-form>
  </div>
</template>

<script>
//  import { type } from 'os'
export default {
  name: 'Login',
  data () {
    return {
      options: [{
        value: 'SUB_BANK',
        label: '支行账户'
      }, {
        value: 'EMPLOYEE',
        label: '员工账户'
      }, {
        value: 'CUSTOMER',
        label: '客户账户'
      }],
      custype: '',
      username: '',
      password: ''
    }
  },
  created () {
    var permission = localStorage.getItem('type')
    if (permission === 'SUB_BANK' || permission === 'EMPLOYEE' || permission === 'CUSTOMER') {
      this.$router.push('/index')
    }
    this.custype = 'SUB_BANK'
  },
  methods: {
    login: function () {
      if (this.username === '' || this.password === '') {
        window.alert('用户密码不嫩为空')
        return
      }
      var _this = this
      _this.$http.post(
        'http://' + document.domain + ':5000/login',
        {
          username: _this.username,
          password: _this.password,
          custype: _this.custype
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        console.log(response.data)
        if (parseInt(response.data.code) === 400) {
          _this.username = ''
          _this.password = ''
          window.alert('登陆失败，请检查用户名和密码是否错误')
        } else if (parseInt(response.data.code) === 200) {
          window.alert('登陆成功')
          localStorage.setItem('type', _this.custype)
          localStorage.setItem('username', _this.username)
          _this.$router.push({path: '/index'})
        } else {
          window.alert('未知错误')
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    register: function () {
      this.$router.push({path: '/register'})
    }
  }
}

</script>

<style scoped>
  .title {
    font-size: 20px;
    color: #303133;
    text-align: center;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
</style>
