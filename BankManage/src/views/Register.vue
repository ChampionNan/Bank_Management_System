<template>
  <div>
  <div class="title">注册界面</div>
    <el-form :model="form" class="form" onsubmit="return false">
      <el-form-item label="账户类型">
        <el-radio v-model="type" label="SUB_BANK" name="type" value="SUB_BANK" aria-required="true">支行账户</el-radio>
        <el-radio v-model="type" label="CUSTOMER" name="type" value="CUSTOMER" aria-required="true">客户账户</el-radio>
        <el-radio v-model="type" label="EMPLOYEE" name="type" value="EMPLOYEE" aria-required="true">员工账户</el-radio>
      </el-form-item>
      <el-form-item v-if="type === 'SUB_BANK'" label="支行名称">
        <el-input class="input" id="username" v-model="username" aria-required="true" placeholder="Please enter the bank name"></el-input>
      </el-form-item>
      <el-form-item v-else label="身份证号">
        <el-input class="input" id="username" v-model="username" aria-required="true" placeholder="Please enter the ID"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'SUB_BANK'" label="所在城市">
        <el-input class="input" id="city" v-model="city" placeholder="Please enter the city name"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'SUB_BANK'" label="资产总额">
        <el-input class="input" id="money" v-model="money" placeholder="Please enter the total money of bank"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'CUSTOMER'" label="姓名">
        <el-input class="input" id="name" v-model="name" placeholder="Please  enter the name of customer"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'CUSTOMER'" label="联系电话">
        <el-input class="input" id="tek" v-model="tel" placeholder="Please  enter the mobile of customer"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'CUSTOMER'" label="家庭住址">
        <el-input class="input" id="addr" v-model="addr" placeholder="Please  enter the address of customer"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'CUSTOMER'" label="联系人姓名">
        <el-input class="input" id="name_link" v-model="name_link" placeholder="Please  enter the name of contact"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'CUSTOMER'" label="联系人手机号">
        <el-input class="input" id="tel_link" v-model="tel_link" placeholder="Please  enter the mobile of contact"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'CUSTOMER'" label="联系人Email">
        <el-input class="input" id="email_link" v-model="email_link" placeholder="Please  enter the Email of contact"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'CUSTOMER'" label="联系人和客户关系">
        <el-input class="input" id="relation" v-model="relation" placeholder="Please  enter the relationship of contact and customer"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'EMPLOYEE'" label="姓名">
        <el-input class="input" id="name" v-model="name" placeholder="Please  enter the name of staff"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'EMPLOYEE'" label="所在部门">
        <el-input class="input" id="dept" v-model="dept" placeholder="Please  enter the department ID of staff"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'EMPLOYEE'" label="所在支行">
        <el-input class="input" id="bankname" v-model="bankname" placeholder="Please  enter the bank name of staff"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'EMPLOYEE'" label="电话号码">
        <el-input class="input" id="tel" v-model="tel" placeholder="Please  enter the mobile of staff"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'EMPLOYEE'" label="家庭住址">
        <el-input class="input" id="addr" v-model="addr" placeholder="Please  enter the address of staff"></el-input>
      </el-form-item>
      <el-form-item v-if="type === 'EMPLOYEE'" label="入职时间">
        <el-input class="input" id="date" v-model="date" placeholder="Please  enter the enter date of staff"></el-input>
      </el-form-item>
      <el-form-item label="6位数字/字母组合密码">
        <el-input class="input" id="password" v-model="password" aria-required="true" placeholder="Please  enter the password" show-password></el-input>
      </el-form-item>
      <el-form-item label="重复6位数字/字母组合密码">
        <el-input class="input" id="password2" v-model="password2" aria-required="true" placeholder="Please  enter the password again" show-password></el-input>
      </el-form-item>
    </el-form>
    <el-button type="prianry" @click.native="submit" round>提交</el-button>
  </div>
</template>

<script>
import XEUtils from 'xe-utils'
//  import XEAjax from 'xe-ajax'
export default {
  name: 'Register',
  data: function () {
    return {
      type: '',
      username: '',
      password: '',
      password2: '',
      name: '',
      city: '',
      money: '',
      tel: '',
      addr: '',
      name_link: '',
      tel_link: '',
      email_link: '',
      relation: '',
      dept: '',
      date: '',
      bankname: ''
    }
  },
  created () {
    this.type = 'SUB_BANK'
  },
  methods: {
    submit: function () {
      if (this.type === '' || this.username === '' || this.password === '') {
        window.alert('必填字段不能为空')
        return
      }
      if (this.password.length !== 6) {
        window.alert('密码长度必须为6位')
        return
      }
      for (var i = 0; i < this.password.length; i++) {
        var x = this.password.charAt(i)
        if (!((x >= '0' && x <= '9') || (x >= 'a' && x <= 'z') || (x >= 'A' && x <= 'Z'))) {
          window.alert('密码非法')
          return
        }
      }
      if (this.password !== this.password2) {
        window.alert('两次输入的密码不同')
      } else {
        this.$http.post(
          'http://' + document.domain + ':5000/register', {
            type: this.type,
            username: this.username,
            password: this.password,
            name: this.name,
            city: this.city,
            money: this.money,
            tel: this.tel,
            addr: this.addr,
            name_link: this.name_link,
            tel_link: this.tel_link,
            email_link: this.email_link,
            relation: this.relation,
            dept: this.dept,
            bankname: this.bankname,
            date_s: XEUtils.toDateString(this.date, 'yyyy-MM-dd')
          }, {
            emulateJSON: true
          }
        ).then(function (response) {
          console.log(parseInt(response.body.code))
          if (parseInt(response.body.code) === 200) {
            localStorage.setItem('type', this.type)
            localStorage.setItem('username', this.username)
            this.$router.push('/index')
            window.alert('注册成功')
          } else if (parseInt(response.body.code) === 400) {
            window.alert('用户名已存在')
          } else {
            window.alert('注册失败')
          }
        })
      }
    }
  }
}

</script>

<style scoped>
  .title {
    text-align: center;
    color: #303133;
    font-size: 20px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
