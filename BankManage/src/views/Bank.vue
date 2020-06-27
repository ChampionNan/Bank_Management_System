<template>
  <div v-loading="loading">
    <el-row>
      <el-col :span="24">
        <div class="title">支行管理</div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="4">
        <div class="subtitle" align="left">1.条件筛选</div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        支行名称<el-input class="input" id="bankSearch" v-model="bankSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="4">
        所在城市<el-input class="input" id="citySearch"  v-model="citySearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="4">
        资产总额下界<el-input type="number" min="0" class="input" id="lowerBound" v-model="lowerBound" placeholder="下界"></el-input>
      </el-col>
      <el-col :span="4">
        资产总额上界<el-input type="number" min="0" class="input" id="upperBound" v-model="upperBound" placeholder="上界"></el-input>
      </el-col>
      <el-col :span="2" style="margin-top: 25px;">
        <el-button size="small" type="primary" @click="submit">查询</el-button>
      </el-col>
      <el-col :span="2" style="margin-top: 25px;">
        <el-button size="small" type="primary" @click="reset">重置</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="4">
        <div class="subtitle">2.支行信息表</div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="4">
        <el-button size="small" type="success" @click="insertEvent">新增</el-button>
        <el-button size="small" type="success" @click="exportCsvEvent">导出</el-button>
      </el-col>
    </el-row>
    <elx-editable ref="elxEditable" class="table" border :data.sync="list" :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod }" style="width: 100%">
      <elx-editable-column type="index" width="55"></elx-editable-column>
      <elx-editable-column prop="name" label="支行名称" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="city" label="所在城市" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="money" label="资产总额" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
      <elx-editable-column label="操作" width="160">
        <template v-slot="scope">
          <template v-if="$refs.elxEditable.hasActiveRow(scope.row)">
            <el-button size="small" type="success" @click="saveRowEvent(scope.row)">保存</el-button>
            <el-button size="small" type="warning" @click="cancelRowEvent(scope.row)">取消</el-button>
          </template>
          <template v-else>
            <el-button size="small" type="primary" @click="openActiveRowEvent(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="removeEvent(scope.row)">删除</el-button>
          </template>
        </template>
      </elx-editable-column>
    </elx-editable>
  </div>
</template>

<script>
import XEUtils from 'xe-utils'
//  import XEAjax from 'xe-ajax'
import {MessageBox, Message} from 'element-ui'
export default {
  name: 'Bank',
  data () {
    return {
      loading: false,
      list: [],
      isClearActiveFlag: '',
      bankSearch: '',
      citySearch: '',
      lowerBound: '',
      upperBound: '',
      permission: '',
      primary: null
    }
  },
  created () {
    this.permission = localStorage.getItem('type')
    if (this.permission !== 'SUB_BANK') {
      //  this.$router.push('/404')
    }
    this.findList()
  },
  methods: {
    findList () {
      this.loading = true
      this.list = []
      this.loading = false
    },
    formatterDate (row, column, cellValue, index) {
      return XEUtils.toDateString(cellValue, 'yyyy-MM-dd HH:mm:ss')
    },
    clearActiveMethod ({type, row}) {
      return false
    },
    insertEvent () {
      console.log('insert')
      let activeInfo = this.$refs.elxEditable.getActiveRow()
      console.log(activeInfo)
      if (!activeInfo) {
        this.$refs.elxEditable.insert({
          name: 'New Bank',
          city: '',
          money: 0
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
            this.primary = row.name
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
          this.primary = row.name
          console.log(row.name)
        }
      })
    },
    cancelRowEvent (row) {
      if (this.primary == null) {
        this.isClearActiveFlag = false
        MessageBox.confirm('该数据未保存，是否移除?', '温馨提示', {
          distinguishCancelAndClose: true,
          confirmButtonText: '移除数据',
          cancelButtonText: '返回继续',
          type: 'warning'
        }).then(action => {
          if (action === 'confirm') {
            this.$refs.elxEditable.remove(row)
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
          if (this.primary == null) {
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
      this.$http.post(
        'http://' + document.domain + ':5000/bank',
        {
          type: 'Delete',
          primary: row.name
        }, {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.$refs.elxEditable.remove(row)
          Message({ message: '删除成功', type: 'success' })
        } else {
          Message({ message: '删除失败，' + response.body.msg, type: 'warning' })
        }
      })
    },
    saveRowEvent (row) {
      this.$refs.elxEditable.validateRow(row, valid => {
        if (valid && this.$refs.elxEditable.hasRowChange(row)) {
          this.$http.post(
            'http://' + document.domain + ':5000/bank',
            {
              type: 'Update',
              name: row.name,
              city: row.city,
              money: row.money,
              old_primary: this.primary
            },
            {
              emulateJSON: true
            }
          ).then(function (response) {
            if (parseInt(response.body.code) === 200) {
              this.primary = null
              this.$refs.elxEditable.clearActive()
              this.$refs.elxEditable.reloadRow(row)
              console.log('Update')
              Message({ message: '保存成功', type: 'success' })
            } else if (parseInt(response.body.code) === 400) {
              Message({ message: '新增记录失败，可能是支行名称重复', type: 'warning' })
            } else {
              Message({ message: '更新失败\n' + response.body.msg, type: 'warning' })
            }
          })
        } else if (valid && !this.$refs.elxEditable.hasRowChange(row)) {
          this.primary = null
          this.$refs.elxEditable.clearActive()
        }
      })
    },
    exportCsvEvent () {
      this.$refs.elxEditable.exportCsv()
    },
    submit () {
      this.$http.post(
        'http://' + document.domain + ':5000/bank',
        {
          type: 'Search',
          bankSearch: this.bankSearch,
          citySearch: this.citySearch,
          lowerBound: this.lowerBound,
          upperBound: this.upperBound
        }, {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.list = response.body.list
          Message({ message: '查询成功', type: 'success' })
        } else {
          Message({ message: '没有查到任何内容', type: 'warning' })
        }
      })
    },
    reset () {
      this.bankSearch = ''
      this.citySearch = ''
      this.lowerBound = ''
      this.upperBound = ''
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
  div {
    color: #606266
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
