<template>
  <div>
    <el-row>
      <el-col :span="24">
        <div class="title">账户管理</div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="4">
        <div class="subtitle" align="left">1.条件筛选</div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        账户号
        <el-input class="input" id="idSearch" v-model="idSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="4">
        户主：<el-input class="input" id="ownerSearch" v-model="ownerSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="4">
        开户银行<el-input class="input" id="bankSearch" v-model="bankSearch" placeholder=""></el-input>
      </el-col>
      <el-col :span="4">
        账户类型
        <el-select v-model="typeSearch" placeholder="any">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        余额下界<el-input type="number" min="0" id="money_lo" class="input" v-model="money_lo" placeholder="下界～"></el-input>
      </el-col>
      <el-col :span="4">
        余额上界<el-input type="number" min="0" id="money_up" class="input" v-model="money_up" placeholder="～上界"></el-input>
      </el-col>
      <el-col :span="4">
        开户日期下界<el-input type="date" min="0" id="open_lo" class="input" v-model="open_lo" placeholder="下界"></el-input>
      </el-col>
      <el-col :span="4">
        开户日期上界<el-input type="date" min="0" id="open_up" class="input" v-model="open_up" placeholder="上界"></el-input>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="20">
        <el-col :span="4">
          <el-button size="small" type="primary" @click="submit">查询</el-button>
        </el-col>
        <el-col :span="4">
          <el-button size="small" type="primary" @click="reset">重置</el-button>
        </el-col>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="6">
        <div class="subtitle" align="left">2.账户信息表 &emsp;
          <el-button size="small" type="success" @click="exportCsvEvent()">导出</el-button>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="6">
        开户者<el-input class="input" id="newownerid" v-model="newownerid" placeholder="身份证号"></el-input>
      </el-col>
      <el-col :span="6">
        账户号<el-input class="input" id="newbankid" v-model="newbankid" placeholder="账户号"></el-input>
      </el-col>
      <el-col :span="6">
        开户支行<el-input class="input" id="newbankname" v-model="newbankname" placeholder="支行名称"></el-input>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="4">账户类型
        <el-select v-model="newtype" placeholder="账户类型">
          <el-option v-for="item in typeList" :key="item.value" :value="item.value" :label="item.label"></el-option>
        </el-select>
      </el-col>
      <el-col v-if="newtype === '0'" :span="4">货币类型
        <el-select v-if="newtype === '0'" v-model="newmoneytype" placeholder="">
          <el-option v-for="item in cachList" :key="item.value" :value="item.value" :label="item.label"></el-option>
        </el-select>
      </el-col>
      <el-col :span="4">
        <div style="margin-top: 28px; margin-left: 0;">
          <el-button type="success" size="small" @click="newaccount">开户</el-button>
          <el-button type="success" size="small" @click="reset2">重置</el-button>
        </div>
      </el-col>
    </el-row>
    <elx-editable ref="elxEditable1" class="table" border :data.sync="list" :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod: clearActiveMethod1 }">
      <elx-editable-column type="index" width="55"></elx-editable-column>
      <elx-editable-column prop="id" label="账户号"></elx-editable-column>
      <elx-editable-column prop="bank" label="开户支行" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="money" label="余额" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="open_date" label="开户日期" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="type" label="账户类型" :edit-render="{ name: 'ElSelect', options: typeList}"></elx-editable-column>
      <elx-editable-column prop="interest" label="利率" :edit-render="{ name: 'ElInputNumber'}"></elx-editable-column>
      <elx-editable-column prop="cashtype" label="货币类型" :edit-render="{ name: 'ElSelect', options: cachList}"></elx-editable-column>
      <elx-editable-column prop="overdraft" label="透支额" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
      <elx-editable-column label="操作" width="250">
        <template v-slot="scope">
          <template v-if=$refs.elxEditable1.hasActiveRow(scope.row)>
            <el-button size="small" type="success" @click="saveRowEvent(scope.row)">保存</el-button>
            <el-button size="small" type="warning" @click="cancelRowEvent(scope.row)">取消</el-button>
          </template>
          <template v-else>
            <el-button size="small" type="primary" @click="openActiveRowEvent(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="removeEvent(scope.row)">销户</el-button>
            <el-button size="small" type="success" @click="showDetail(scope.row)">查看户主</el-button>
          </template>
        </template>
      </elx-editable-column>
    </elx-editable>
    <div v-if="showlink">
      <p style="color: gray;font-size: 24px;" align="left">
        户主信息表
        <el-button type="success" size="small" @click="showlink = false">关闭</el-button>
      </p>
      <div align="left">
        新增户主 <el-input min="0" id="newOwner" v-model="newOwner" placeholder="身份证号"></el-input>
        <el-button size="small" type="success" @click="addOwner">提交</el-button>
      </div>
      <elx-editable ref="elxEditable2" class="table" border :data.sync="ownerlist" :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod: clearActiveMethod2 }" style="width: 100%">
        <elx-editable-column type="index" width="55"></elx-editable-column>
        <elx-editable-column prop="id" label="账户号"></elx-editable-column>
        <elx-editable-column prop="bank" label="开户银行"></elx-editable-column>
        <elx-editable-column prop="ownerid" label="户主身份证号"></elx-editable-column>
        <elx-editable-column prop="ownername" label="户主姓名"></elx-editable-column>
        <elx-editable-column prop="visit_date" label="最近访问日期" :edit-render="{name: 'ElDatePicker', props: { type: 'date', format: 'yyyy-MM-dd' }}"></elx-editable-column>
        <elx-editable-column label="操作" width="160">
          <template v-slot="scope">
            <el-button size="small" type="danger" @click="removeOwner(scope.row)">删除</el-button>
          </template>
        </elx-editable-column>
      </elx-editable>
    </div>
  </div>
</template>

<script>
import XEUtils from 'xe-utils'
//  import XEAjax from 'xe-ajax'
import { MessageBox, Message } from 'element-ui'
export default {
  name: 'Account',
  data () {
    return {
      options: [{
        value: 'any',
        label: 'any'
      }, {
        value: 'saving',
        label: 'saving'
      }, {
        check: 'check',
        label: 'check'
      }],
      typeList: [{
        value: '0',
        label: '储蓄账户'
      }, {
        value: '1',
        label: '支票账户'
      }],
      cachList: [{
        value: '0',
        label: '人命币'
      }, {
        value: '1',
        label: '美元'
      }, {
        value: '2',
        label: '欧元'
      }, {
        value: '3',
        label: '日元'
      }],
      loading: false,
      newbankname: '',
      newmoneytype: '0',
      newbankid: '',
      newtype: '0',
      showlink: false,
      newOwner: '',
      detail: '',
      ownerlist: [],
      list: [],
      isClearActiveFlag: true,
      bankSearch: '',
      idSearch: '',
      ownerSearch: '',
      typeSearch: '',
      money_lo: '',
      money_up: '',
      open_lo: '',
      open_up: '',
      visit_lo: '',
      visit_up: '',
      permission: '',
      newownerid: '',
      primary: null //  全局变量，记录修改前主键
    }
  },
  created () {
    this.permission = localStorage.getItem('type')
    if (this.permission !== 'EMPLOYEE' && this.permission !== 'SUB_BANK' && this.permission !== 'CUSTOMER') {
      this.$router.push('/404')
    }
    this.findList()
    this.typeSearch = 'any'
  },
  methods: {
    findList () {
      this.loading = true
      this.list = []
      this.loading = false
    },
    activeMethod ({ row, column }) {
      if (column.label === '账户号' || column.label === '开户支行' || column.label === '账户类型' || column.label === '货币类型') {
        return false
      }
      if (row.type === '0' && column.label === '透支额') {
        return false
      }
      if (row.type === '1' && column.label === '利率') {
        return false
      }
      return true
    },
    clearActiveMethod2 ({ type, row, rowIndex }) {
      return false
    },
    formatterDate (row, column, cellValue, index) {
      return XEUtils.toDateString(cellValue, 'yyyy-MM-dd')
    },
    newaccount () {
      if (this.newbankid === '' || this.newbankname === '' || this.newownerid === '') {
        return
      }
      this.$http.post(
        'http://' + document.domain + ':5000/account',
        {
          type: 'Update',
          id: this.newbankid,
          bank: this.newbankname,
          money: 0,
          ownerid: this.newownerid,
          open_date: XEUtils.toDateString(new Date(), 'yyyy-MM-dd'),
          acctype: this.newtype,
          interest: 0,
          cashtype: this.newmoneytype,
          overdraft: 0,
          old_primary: null
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        console.log(parseInt(response.body.code))
        window.alert(parseInt(response.body.code))
        if (parseInt(response.body.code) === 200) {
          this.$refs.elxEditable1.insert({
            id: this.newbankid,
            bank: this.newbankname,
            money: 0,
            open_date: XEUtils.toDateString(new Date(), 'yyyy-MM-dd'),
            type: this.newtype,
            interest: null,
            cashtype: this.newmoneytype,
            overdraft: null
          })
          Message({message: '开户成功', type: 'success'})
        } else {
          Message({message: '开户失败,提供的信息可能有误或您已经在该支行开设同类账户', type: 'warning'})
        }
      })
    },
    insertEvent () {
      console.log('insert')
      let activeInfo = this.$refs.elxEditable1.getActiveRow()
      console.log(activeInfo)
      if (!activeInfo) {
        this.$refs.elxEditable1.insert({
          id: 'new id',
          owner: '',
          bank: '',
          money: 0,
          open_date: XEUtils.toDateString(new Date(), 'yyyy-MM-dd'),
          type: '0',
          interest: null,
          cashtype: null,
          overdraft: null
        }).then(({ row }) => {
          this.$refs.elxEditable1.setActiveRow(row)
        })
      }
    },
    openActiveRowEvent (row) {
      this.$nextTick(() => {
        let activeInfo = this.$refs.elxEditable1.getActiveRow()
        if (activeInfo && activeInfo.isUpdate) {
          this.isClearActiveFlag = false
          MessageBox.confirm('检测到未保存的内容，请确认操作?', '温馨提示', {
            distinguishCancelAndClose: true,
            confirmButtonText: '保存数据',
            cancelButtonText: '取消修改',
            type: 'warning'
          }).then(() => {
            this.$refs.elxEditable1.setActiveRow(row)
            this.primary = row.id
            this.saveRowEvent(activeInfo.row)
          }).catch(action => {
            if (action === 'cancel') {
              this.$refs.elxEditable1.revert(activeInfo.row)
              this.$refs.elxEditable1.setActiveRow(row)
            }
          }).then(() => {
            this.isClearActiveFlag = true
          })
        } else {
          this.$refs.elxEditable1.setActiveRow(row)
          this.primary = row.id
          console.log(row.id)
        }
      })
    },
    cancelRowEvent (row) {
      this.isClearActiveFlag = false
      MessageBox.confirm('该数据未保存，是否移除?', '温馨提示', {
        distinguishCancelAndClose: true,
        confirmButtonText: '放弃修改',
        cancelButtonText: '返回继续',
        type: 'warning'
      }).then(action => {
        if (action === 'confirm') {
          this.$refs.elxEditable1.clearActive()
          this.$refs.elxEditable1.revert(row)
          if (this.primary === null) {
            this.$refs.elxEditable.remove(row)
          }
          this.primary = null
        }
      }).catch(action => action).then(() => {
        this.isClearActiveFlag = true
      })
    },
    removeEvent (row) {
      this.$http.post(
        'http://' + document.domain + ':5000/account',
        {
          type: 'Delete',
          primary: row.id,
          acctype: row.type
        }, {
          emulateJSON: true
        }
      ).then(function (response) {
        console.log(parseInt(response.body.code))
        if (parseInt(response.body.code) === 200) {
          Message({message: '删除成功', type: 'success'})
          this.$refs.elxEditable.remove(row)
        } else {
          Message({message: '删除失败', type: 'warning'})
        }
      })
    },
    saveRowEvent (row) {
      if (this.$refs.elxEditable1.hasRowChange(row)) {
        this.$http.post(
          'http://' + document.domain + ':5000/account',
          {
            type: 'Update',
            id: row.id,
            bank: row.bank,
            money: row.money,
            ownerid: null,
            open_date: row.open_date,
            acctype: row.type,
            interest: row.interest,
            cashtype: row.cashtype,
            overdraft: row.overdraft,
            old_primary: row.id
          }, {
            emulateJSON: true
          }
        ).then(function (response) {
          console.log(parseInt(response.body.code))
          if (parseInt(response.body.code) === 200) {
            this.$refs.elxEditable1.clearActive()
            this.$refs.elxEditable1.reloadRow(row)
            Message({message: '保存成功', type: 'success'})
          } else {
            Message({message: '保存失败，可能是账户号已存在', type: 'warning'})
          }
        })
      }
    },
    exportCsvEvent () {
      this.$refs.elxEditable1.exportCsv()
    },
    submit () {
      this.showlink = false
      this.$http.post(
        'http://' + document.domain + ':5000/account',
        {
          type: 'Search',
          bankSearch: this.bankSearch,
          idSearch: this.idSearch,
          ownerSearch: this.ownerSearch,
          typeSearch: this.typeSearch,
          money_lo: this.money_lo,
          money_up: this.money_up,
          open_lo: XEUtils.toDateString(this.open_lo, 'yyyy-MM-dd'),
          open_up: XEUtils.toDateString(this.open_up, 'yyyy-MM-dd'),
          visit_lo: XEUtils.toDateString(this.visit_lo, 'yyyy-MM-dd'),
          visit_up: XEUtils.toDateString(this.visit_up, 'yyyy-MM-dd')
        }, {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.list = response.body.list
          Message({message: '查询成功', type: 'success'})
        } else {
          Message({message: '查询结果为空', type: 'warning'})
        }
      })
    },
    reset () {
      this.bankSearch = ''
      this.idSearch = ''
      this.ownerSearch = ''
      this.typeSearch = ''
      this.money_lo = ''
      this.money_up = ''
      this.open_lo = ''
      this.open_up = ''
      this.visit_lo = ''
      this.visit_up = ''
    },
    addOwner () {
      if (this.newOwner === '') {
        return
      }
      this.$http.post(
        'http://' + document.domain + ':5000/accountCustomer',
        {
          type: 'Insert',
          accid: this.detail.id,
          bank: this.detail.bank,
          visit_date: XEUtils.toDateString(new Date(), 'yyyy-MM-dd'),
          ownerid: this.newOwner,
          acctype: this.detail.type
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        console.log(parseInt(response.body.code))
        if (parseInt(response.body.code) === 200) {
          this.ownerlist.push(response.body.record)
          Message({message: '新增户主成功', type: 'success'})
        } else {
          Message({message: '新增户主失败，可能是身份证号错误或其已经在该支行开设同类账户', type: 'warning'})
        }
      })
    },
    removeOwner (row) {
      this.$http.post(
        'http://' + document.domain + ':5000/accountCustomer',
        {
          type: 'Delete',
          accid: this.detail.id,
          bank: this.detail.bank,
          ownerid: row.ownerid,
          acctype: this.detail.type
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.$refs.elxEditable2.remove(row)
          Message({message: '删除成功', type: 'success'})
        } else {
          window.alert('删除失败')
        }
      })
    },
    searchOwner (row) {
      this.$http.post(
        'http://' + document.domain + ':5000/accountCustomer',
        {
          type: 'Search',
          accid: this.detail.id,
          bank: row.bank,
          acctype: row.type
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.ownerlist = response.body.list
          for (var i = 0; i < this.ownerlist.length; i++) {
            this.ownerlist[i].id = row.id
            this.ownerlist[i].bank = row.bank
          }
          Message({message: '查询成功', type: 'success'})
        } else {
          this.ownerlist = []
          Message({message: '查询失败', type: 'error'})
        }
      })
    },
    showDetail (row) {
      this.showlink = true
      this.detail = row
      console.log('update')
      console.log(row.id)
      this.searchOwner(row)
    },
    reset2 () {
      this.newbankname = ''
      this.newmoneytype = '0'
      this.newbankid = ''
      this.newtype = ''
      this.newownerid = ''
    }
  }
}

</script>

<style scoped>
  div {
    color: #606266
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
  .title {
    text-align: center;
    color: #F56C6C;
    font-size: 28px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
  .subtitle {
    text-align: center;
    color: #E6A23C;
    font-size: 20px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
</style>
