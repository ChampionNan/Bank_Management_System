<template>
  <div v-loading="laoding">
    <el-row>
      <el-col :span="24">
        <div class="title">贷款管理</div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        <div class="subtitle">1.条件筛选</div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="6">
        贷款号<el-input v-model="idSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="6">
        放款支行<el-input v-model="bankSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="6">
        贷款人<el-input v-model="custSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="6">
        状态<el-select v-model="statusSearch" placeholder="请选择" style="margin-top: 20px;">
          <el-option v-for="item in options" :key="item.value" :value="item.value" :label="item.label"></el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="6">
        金额下界<el-input v-model="lowerBound" placeholder="下界"></el-input>
      </el-col>
      <el-col :span="6">
        金额上界<el-input v-model="upperBound" placeholder="上界"></el-input>
      </el-col>
      <el-col :span="2">
        <el-button size="small" type="primary" @click="submit" style="margin-top: 25px;">查询</el-button>
      </el-col>
      <el-col :span="2">
        <el-button size="small" type="primary" @click="reset" style="margin-top: 25px;">重置</el-button>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        <div class="subtitle">2.贷款信息表</div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="2">
        <el-button size="small" type="success" @click="exportCsvEvent">导出</el-button>
      </el-col>
      <el-col :span="2">
        <el-button size="small" type="success" @click="insertEvent">发放贷款</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="8"><font style="color: red" align="left" v-if="messageshow">请在贷款人字段填写所有贷款人的身份证号，并使用英文逗号分隔</font></el-col>
    </el-row>
    <elx-editable ref="elxEditable" class="table" border :data.sync="list" :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod }" style="width: 100%;">
      <elx-editable-column type="index" width="55"></elx-editable-column>
      <elx-editable-column prop="id" label="贷款号" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="bank" label="放款支行" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="customer" label="贷款人" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="amount" label="金额" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
      <elx-editable-column prop="status" label="状态"></elx-editable-column>
      <elx-editable-column label="操作" width="260">
        <template v-slot="scope">
            <template v-if="$refs.elxEditable.hasActiveRow(scope.row)">
                <el-button size="small" type="success" @click="saveRowEvent(scope.row)">保存</el-button>
                <el-button size="small" type="warning" @click="cancelRowEvent(scope.row)">取消</el-button>
            </template>
            <template v-else>
                <el-button size="small" type="danger" @click="removeEvent(scope.row)">删除</el-button>
                <el-button size="small" type="success" @click="showDetail(scope.row)">详情</el-button>
            </template>
        </template>
      </elx-editable-column>
    </elx-editable>
    <div v-if="showlink">
      <el-row>
        <el-col :span="4">
          <p class="subtitle" align="left">3.支付信息表
            <el-button type="success" size="small" @click="showlink = false">关闭</el-button>
          </p>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          进行支付<el-input type="number" min="0" v-model="payAmount" placeholder="金额"></el-input>
        </el-col>
        <el-col :span="2">
          <el-button size="small" type="success" @click="newpay" style="margin-top: 25px;">支付</el-button>
        </el-col>
      </el-row>
      <elx-table ref="elxTable" border size="small" :data.sync="paylist" style="width: 100%;">
        <elx-table-column type="index" width="55"></elx-table-column>
        <elx-table-column prop="id" label="贷款号"></elx-table-column>
        <elx-table-column prop="date_s" label="支付日期" :formatter="formatterDate"></elx-table-column>
        <elx-table-column prop="money" label="支付金额"></elx-table-column>
      </elx-table>
    </div>
  </div>
</template>

<script>
import XEUtils from 'xe-utils'
//  import XEAjax from 'xe-ajax'
import { MessageBox, Message } from 'element-ui'
export default {
  data () {
    return {
      options: [{
        value: 'any',
        label: '任意'
      }, {
        value: 'none',
        label: '未开始发放'
      }, {
        value: 'part',
        label: '发放中'
      }, {
        value: 'all',
        label: '已全部发放'
      }],
      laoding: false,
      list: [],
      statusList: ['未开始发放', '发放中', '已全部发放'],
      paylist: [],
      showlink: false,
      showpay: false,
      isClearActiveFlag: true,
      bankSearch: '',
      idSearch: '',
      statusSearch: 'any',
      custSearch: '',
      upperBound: '',
      lowerBound: '',
      detail: '',
      payAmount: '',
      messageshow: false,
      permission: '',
      primary: null
    }
  },
  created () {
    this.permission = localStorage.getItem('type')
    if (this.permission !== 'EMPLOYEE' && this.permission !== 'SUB_BANK' && this.permission !== 'CUSTOMER') {
      //  this.$router.push('/404')
    }
    this.findList()
    this.statusSearch = 'any'
  },
  methods: {
    findList () {
      this.laoding = true
      this.list = []
      this.laoding = false
    },
    formatterDate (row, column, cellValue, index) {
      return XEUtils.toDateString(cellValue, 'yyyy-MM-dd')
    },
    clearActiveMethod ({ type, row }) {
      return false
    },
    showDetail (row) {
      this.showlink = true
      this.detail = row
      this.$http.post(
        'http://' + document.domain + ':5000/pay',
        {
          type: 'Search',
          loanid: row.id
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.paylist = response.body.list
          for (var i = 0; i < this.paylist.length; i++) {
            this.paylist[i].id = row.id
          }
          Message({ message: '查询成功', type: 'success' })
        } else {
          Message({ message: '查询结果为空', type: 'warning' })
          this.paylist = []
        }
      })
    },
    newpay () {
      if (this.payAmount === '') {
        Message({ message: '支付金额不能为空', type: 'warning' })
        return
      }
      var sum = parseInt(this.payAmount)
      for (var i = 0; i < this.paylist.length; i++) {
        sum = sum + parseInt(this.paylist[i].money)
      }
      console.log(sum, this.detail.amount)
      if (sum > this.detail.amount) {
        Message({ message: '支付超额', type: 'warning' })
        return
      }
      this.$http.post(
        'http://' + document.domain + ':5000/pay',
        {
          type: 'Insert',
          loanid: this.detail.id,
          date: XEUtils.toDateString(new Date(), 'yyyy-MM-dd'),
          money: this.payAmount
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        console.log(parseInt(response.body.code))
        if (parseInt(response.body.code) === 200) {
          this.paylist.push({ id: this.detail.id, date_s: XEUtils.toDateString(new Date(), 'yyyy-MM-dd'), money: this.payAmount })
          var sum = 0
          for (var i = 0; i < this.paylist.length; i++) {
            sum = sum + parseInt(this.paylist[i].money)
          }
          if (sum < this.detail.amount) {
            this.detail.status = '发放中'
          } else if (sum === 0) {
            this.detail.status = '未开始发放'
          } else {
            this.detail.status = '已全部发放'
          }
          Message({ message: '支付成功', type: 'success' })
        } else {
          Message({ message: '支付失败，可能超额', type: 'warning' })
        }
      })
    },
    insertEvent () {
      console.log('insert')
      this.messageshow = true
      let activeInfo = this.$refs.elxEditable.getActiveRow()
      console.log(activeInfo)
      if (!activeInfo) {
        this.$refs.elxEditable.insert({
          id: 'new id',
          bank: '',
          customer: '',
          amount: 0,
          status: '未开始发放'
        }).then(({ row }) => {
          this.$refs.elxEditable.setActiveRow(row)
        })
      }
    },
    openActiveRowEvent (row) {
      this.$nextTick(() => {
        let activeInfo = this.$refs.elxEditable.getActiveRow()
        if (activeInfo && activeInfo.isUpdate) {
          this.isClearActiveFlag = false
          MessageBox.confirm('检测到未保存的内容，请确认操作?', '温馨提示', {
            distinguishCancelAndClose: true,
            confirmButtonText: '保存数据',
            cancelButtonText: '取消修改',
            type: 'warning'
          }).then(() => {
            this.$refs.elxEditable.setActiveRow(row)
            this.primary = row.id
            this.saveRowEvent(activeInfo.row)
          }).catch(action => {
            if (action === 'cancel') {
              this.$refs.elxEditable.revert(activeInfo.row)
              this.$refs.elxEditable.setActiveRow(row)
            }
          }).then(() => {
            this.isClearActiveFlag = true
          })
        } else {
          this.$refs.elxEditable.setActiveRow(row)
          this.primary = row.id
          console.log(row.id)
        }
      })
    },
    cancelRowEvent (row) {
      if (this.primary === null) {
        this.isClearActiveFlag = false
        MessageBox.confirm('该数据未保存，是否移除?', '温馨提示', {
          distinguishCancelAndClose: true,
          confirmButtonText: '移除数据',
          cancelButtonText: '返回继续',
          type: 'warning'
        }).then(action => {
          if (action === 'confirm') {
            this.$refs.elxEditable.remove(row)
            this.messageshow = false
          }
        }).catch(action => action).then(() => {
          this.isClearActiveFlag = true
        })
      } else if (this.$refs.elxEditable.hasRowChange(row)) {
        this.isClearActiveFlag = false
        MessageBox.confirm('检测到未保存的内容，是否取消修改?', '温馨提示', {
          distinguishCancelAndClose: true,
          confirmButtonText: '取消修改',
          cancelButtonText: '返回继续',
          type: 'warning'
        }).then(action => {
          this.$refs.elxEditable.clearActive()
          this.$refs.elxEditable.revert(row)
          if (this.primary === null) {
            this.$refs.elxEditable.remove(row)
          }
          this.primary = null
        }).catch(action => {
          if (action === 'cancel') {
            this.$refs.elxEditable.setActiveRow(row)
          }
        }).then(() => {
          this.isClearActiveFlag = true
        })
      } else {
        this.$refs.elxEditable.clearActive()
      }
    },
    removeEvent (row) {
      if (row.status === '发放中') {
        Message({ message: '发放中的贷款不能删除', type: 'warning' })
        return
      }
      this.$http.post(
        'http://' + document.domain + ':5000/loan',
        {
          type: 'Delete',
          primary: row.id
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.$refs.elxEditable.remove(row)
          Message({ message: '删除成功', type: 'success' })
        } else {
          Message({ message: '发放中的贷款不能删除', type: 'warning' })
        }
      })
    },
    saveRowEvent (row) {
      console.log('save')
      console.log(row)
      if (row.id === '' || row.bank === '' || row.customer === '' || row.amount < 0) {
        Message({ message: '字段不能为空', type: 'warning' })
        return
      }
      this.messageshow = false
      this.$refs.elxEditable.validateRow(row, valid => {
        if (valid && this.$refs.elxEditable.hasRowChange(row)) {
          this.$http.post(
            'http://' + document.domain + ':5000/loan',
            {
              type: 'Update',
              id: row.id,
              bank: row.bank,
              customer: row.customer,
              amount: row.amount,
              status: this.statusList.indexOf(row.status),
              old_primary: this.primary
            },
            {
              emulateJSON: true
            }
          ).then(function (response) {
            console.log(parseInt(response.body.code))
            if (parseInt(response.body.code) === 200) {
              this.priamry = null
              row.customer = response.body.customer
              this.$refs.elxEditable.clearActive()
              this.$refs.elxEditable.reloadRow(row)
              Message({ message: '发放贷款成功', type: 'success' })
            } else {
              Message({ message: '发放贷款失败,可能是输入信息错误', type: 'warning' })
            }
          })
        } else if (valid && !this.$refs.elxEditable.hasRowChange(row)) {
          this.priamry = null
          this.$refs.elxEditable.clearActive()
        }
      })
    },
    exportCsvEvent () {
      this.$refs.elxEditable.exportCsv()
    },
    submit () {
      this.$http.post(
        'http://' + document.domain + ':5000/loan',
        {
          type: 'Search',
          idSearch: this.idSearch,
          bankSearch: this.bankSearch,
          statusSearch: this.statusSearch,
          custSearch: this.custSearch,
          upperBound: this.upperBound,
          lowerBound: this.lowerBound
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        console.log(response.body.list)
        if (parseInt(response.body.code) === 200) {
          this.list = response.body.list
          for (var i = 0; i < response.data.list.length; i++) {
            var t = this.list[i].status
            this.list[i].status = this.statusList[t]
          }
          this.showlink = false
          Message({ message: '查询成功', type: 'success' })
        } else {
          this.showlink = false
          Message({ message: '查询结果为空', type: 'warning' })
        }
      })
    },
    reset () {
      this.bankSearch = ''
      this.idSearch = ''
      this.statusSearch = ''
      this.custSearch = ''
      this.upperBound = ''
      this.lowerBound = ''
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
    font-size: 24px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
  .subtitle {
    text-align: center;
    color: #E6A23C;
    font-size: 20px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
</style>
