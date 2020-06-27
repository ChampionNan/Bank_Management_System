<template>
  <div>
    <el-row>
      <el-col :span="24"><h1 class="title">银行管理系统</h1></el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <div v-html="message" class="subtitle"></div>
      </el-col>
    </el-row>
    <el-row v-if="type == 'SUB_BANK'">
      <el-col :span="24">
        <el-button @click.native="goBank" type="primary">支行管理</el-button>
      </el-col>
    </el-row>
    <el-row v-if="type == 'EMPLOYEE' || type == 'SUB_BANK'">
      <el-col :span="24">
        <el-button @click.native="goStaff" type="primary">员工管理</el-button>
      </el-col>
    </el-row>
    <el-row v-if="type == 'SUB_BANK' || type == 'CUSTOMER'">
      <el-col :span="24">
        <el-button @click.native="goCustomer" type="primary">客户管理</el-button>
      </el-col>
    </el-row>
    <el-row v-if="type == 'SUB_BANK' || type == 'EMPLOYEE' || type == 'CUSTOMER'">
      <el-col :span="24">
        <el-button @click.native="goAccount" type="primary">账户管理</el-button>
      </el-col>
    </el-row>
    <el-row v-if="type == 'SUB_BANK' || type == 'EMPLOYEE' || type == 'CUSTOMER'">
      <el-col :span="24">
        <el-button @click.native="goLoan" type="primary">贷款管理</el-button>
      </el-col>
    </el-row>
    <el-row v-if="type == 'SUB_BANK'">
      <el-col :span="24">
        <el-button @click.native="goSummary" type="primary">业务统计</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-button @click.native="exit" type="danger">退出登录</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'index',
  data () {
    return {
      type: '',
      message: ''
    }
  },
  created () {
    this.type = localStorage.getItem('type')
    if (this.type !== 'EMPLOYEE' && this.type !== 'SUB_BANK' && this.type !== 'CUSTOMER') {
      //  this.$router.push('/404')
    }
    switch (this.type) {
      case 'SUB_BANK':
        this.message = '<h2>账户类型：支行账户</h2><h2>支行名' + localStorage.getItem('username') + '</h2>'
        break
      case 'EMPLOYEE':
        this.message = '<h2>账户类型：员工账户</h2><h2>身份证号' + localStorage.getItem('username') + '</h2>'
        break
      case 'CUSTOMER':
        this.message = '<h2>账户类型：客户账户</h2><h2>身份证号' + localStorage.getItem('username') + '</h2>'
        break
    }
    console.log(this.type)
  },
  methods: {
    goSummary: function () {
      this.$router.push('/summary')
    },
    goBank: function () {
      this.$router.push('/bank')
    },
    goStaff: function () {
      this.$router.push('/staff')
    },
    goCustomer: function () {
      this.$router.push('/customer')
    },
    goAccount: function () {
      this.$router.push('/account')
    },
    goLoan: function () {
      this.$router.push('/loan')
    },
    exit: function () {
      localStorage.setItem('type', null)
      this.$router.push('/')
    }
  }
}

</script>

<style scoped>
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
  .title {
    text-align: center;
    color: #F56C6C;
    font-size: 28px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
  .subtitle {
    text-align: center;
    color: #E6A23C;
    font-size: 15px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
</style>
