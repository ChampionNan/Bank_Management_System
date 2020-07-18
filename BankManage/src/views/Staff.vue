<template>
  <div v-loading="loading">
    <el-row>
      <el-col :span="24">
        <div class="title">员工管理</div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        <div class="subtitle">1.条件筛选</div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="6">
        身份证号<el-input v-model="idSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="6">
        姓名<el-input v-model="nameSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="6">
        所属支行<el-input v-model="bankSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="6">
        所在部门<el-input v-model="deptSearch" placeholder="包含关键字"></el-input>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="6">
        电话号码<el-input v-model="telSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="6">
        家庭住址<el-input v-model="addrSearch" placeholder="包含关键字"></el-input>
      </el-col>
      <el-col :span="6">
        入职日期下界<el-input v-model="lowerBound" placeholder="下界"></el-input>
      </el-col>
      <el-col :span="6">
        入职日期上界<el-input v-model="upperBound" placeholder="上界"></el-input>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="2">
        <el-button size="small" type="primary" @click="submit" >查询</el-button>
      </el-col>
      <el-col :span="2">
        <el-button size="small" type="primary" @click="reset">重置</el-button>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        <div class="subtitle">2.员工信息表</div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="2">
        <el-button size="small" type="success" @click="insertEvent('elxEditable1')" v-if="permission == 'SUB_BANK'">新增</el-button>
      </el-col>
      <el-col :span="2">
        <el-button size="small" type="success" @click="exportCsvEvent('elxEditable1')">导出</el-button>
      </el-col>
    </el-row>
    <elx-editable ref="elxEditable1" class="table" border :data.sync="list" :edit-config="{ trigger: 'manual', mode:'row', clearActiveMethod: clearActiveMethod1 }">
      <elx-editable-column type="index"></elx-editable-column>
      <elx-editable-column prop="id" label="身份证号" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="name" label="姓名" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="bank" label="所属支行" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="dept" label="所在部门" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="tel" label="电话号码" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="addr" label="家庭住址" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
      <elx-editable-column prop="date_s" label="入职日期" :edit-render="{name: 'ElDatePicker', props: { type: 'date', format: 'yyyy-MM-dd' }}"></elx-editable-column>
      <elx-editable-column>
        <template v-slot="scope">
          <template v-if="$refs.elxEditable1.hasActiveRow(scope.row)">
            <el-button size="small" type="success" @click="saveRowEvent('elxEditable1', scope.row)">保存</el-button>
            <el-button size="small" type="warning" @click="cancelRowEvent('elxEditable1', scope.row)">取消</el-button>
          </template>
          <template v-else>
            <el-button size="small" type="primary" @click="openActiveRowEvent('elxEditable1', scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="removeEvent('elxEditable1', scope.row)" v-if="permission == 'SUB_BANK'">删除</el-button>
            <el-button size="small" type="success" @click="showDetail(scope.row)">详情</el-button>
          </template>
        </template>
      </elx-editable-column>
    </elx-editable>
    <div v-if="showlink">
      <el-row :gutter="20">
        <el-col :span="4"><div class="subtitle" style="margin-top: 25px;">3.客户联系表</div></el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="2">
          <el-button size="small" type="success" @click="insertEvent('elxEditable2')">新增</el-button>
        </el-col>
        <el-col :span="2">
          <el-button size="small" type="success" @click="exportCsvEvent('elxEditable2')">导出</el-button>
        </el-col>
        <el-col :span="2">
          <el-button size="small" type="warning" @click="showlink = false">关闭</el-button>
        </el-col>
      </el-row>
      <elx-editable ref="elxEditable2" class="table" border :data.sync="linklist" :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod: clearActiveMethd2}" style="width: 100%;">
        <elx-editable-column type="index" width="55"></elx-editable-column>
        <elx-editable-column prop="staffid" label="员工身份证号"></elx-editable-column>
        <elx-editable-column prop="staffname" label="员工姓名"></elx-editable-column>
        <elx-editable-column prop="id" label="客户身份证号" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
        <elx-editable-column prop="name" label="客户姓名"></elx-editable-column>
        <elx-editable-column prop="type" label="与客户关系" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
        <elx-editable-column label="操作" width="160">
          <template v-slot="newscope">
              <template v-if="$refs.elxEditable2.hasActiveRow(newscope.row)">
                  <el-button size="small" type="success" @click="saveRowEvent('elxEditable2', newscope.row)">保存</el-button>
                  <el-button size="small" type="warning" @click="cancelRowEvent('elxEditable2', newscope.row)">取消</el-button>
              </template>
              <template v-else>
                  <el-button size="small" type="primary" @click="openActiveRowEvent('elxEditable2', newscope.row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="removeEvent('elxEditable2', newscope.row)">删除</el-button>
              </template>
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
  data () {
    return {
      loading: false,
      list: [],
      linklist: [],
      serviceList: [{
        label: '银行负责人',
        value: '0'
      }, {
        label: '贷款负责人',
        value: '1'
      }],
      isClearActiveFlag: true,
      nameSearch: '',
      idSearch: '',
      bankSearch: '',
      deptSearch: '',
      telSearch: '',
      addrSearch: '',
      lowerBound: '',
      upperBound: '',
      showlink: '',
      detail: '',
      detailName: '',
      permission: '',
      primary: null
    }
  },
  created () {
    this.permission = localStorage.getItem('type')
    if (this.permission !== 'SUB_BANK' && this.permission !== 'EMPLOYEE') {
      this.$router.push('/404')
    }
    this.findList()
  },
  methods: {
    findList () {
      this.loading = true
      this.list = []
      this.linklist = []
      this.loading = false
    },
    formatterDate (row, column, cellValue, index) {
      return XEUtils.toDateString(cellValue, 'yyyy-MM-dd')
    },
    clearActiveMethod1 ({ type, row, rowIndex }) {
      return this.isClearActiveFlag && type === 'out' ? this.checkSaveData('elxEditable1', row) : this.isClearActiveFlag
    },
    clearActiveMethd2 ({ type, row, rowIndex }) {
      return this.isClearActiveFlag && type === 'out' ? this.checkSaveData('elxEditable2', row) : this.isClearActiveFlag
    },
    insertEvent (name) {
      let activeInfo = this.$refs[name].getActiveRow()
      if (!activeInfo) {
        if (name === 'elxEditable1') {
          this.$refs[name].insert().then(({ row }) => {
            this.$refs[name].setActiveRow(row)
          })
        } else
        if (this.permission !== 'SUB_BANK' && this.detail.id !== localStorage.getItem('username')) {
          Message({message: '您没有操作权限', type: 'warning'})
          return
        }
        this.$refs[name].insert({staffid: this.detail.id, staffname: this.detail.name}).then(({ row }) => {
          this.$refs[name].setActiveRow(row)
        })
      }
    },
    customExportCsvEvent (name, opts) {
      this.$refs[name].exportCsv(opts)
    },
    exportCsvEvent (name) {
      this.$refs[name].elxEditable.exportCsv()
    },
    submit () {
      this.showlink = false
      this.$http.post(
        'http://' + document.domain + ':5000/staff',
        {
          type: 'Search',
          nameSearch: this.nameSearch,
          idSearch: this.idSearch,
          bankSearch: this.bankSearch,
          deptSearch: this.deptSearch,
          telSearch: this.telSearch,
          addrSearch: this.addrSearch,
          lowerBound: this.lowerBound,
          upperBound: this.upperBound
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.list = response.body.list
          Message({ message: '查询成功', type: 'success' })
        } else {
          Message({ message: '查询失败', type: 'warning' })
        }
      })
    },
    reset () {
      this.nameSearch = ''
      this.idSearch = ''
      this.deptSearch = ''
      this.telSearch = ''
      this.addrSearch = ''
      this.lowerBound = ''
      this.upperBound = ''
    },
    showDetail (row) {
      this.showlink = true
      this.detail = row
      this.$http.post(
        'http://' + document.domain + ':5000/staffCustomer',
        {
          type: 'SearchByStaff',
          staffid: row.id
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.linklist = response.body.list
          for (var i = 0; i < this.linklist.length; i++) {
            this.linklist[i].staffname = row.name
            this.linklist[i].staffid = row.id
          }
          Message({ message: '查询成功', type: 'success' })
        } else {
          this.linklist = []
          Message({ message: '没有查到任何记录', type: 'warning' })
        }
      })
    },
    checkSaveData (name, row) {
      if (this.$refs[name].hasRowChange(row)) {
        this.isClearActiveFlag = false
        MessageBox.confirm('您离开了表格，检测未保存的内容，是否在离开前保存修改?', '温馨提示', {
          closeOnClickModal: false,
          distinguishCancelAndClose: true,
          confirmButtonText: '保存',
          cancelButtonText: '放弃修改',
          type: 'warning'
        }).then(() => {
          this.saveRowEvent(name, row)
        }).catch(action => {
          if (action === 'cancel') {
            this.$refs[name].revert(row)
            this.$refs[name].clearActive()
            if (this.primary === null) {
              this.$refs[name].remove(row)
            }
            this.primary = null
            Message({ message: '放弃修改并离开当前行', type: 'warning' })
          } else {
            this.$refs[name].setActiveRow(row)
            Message({ message: '停留在当前行编辑', type: 'info' })
          }
        }).then(() => {
          this.isClearActiveFlag = true
        })
        return false
      } else {
        this.primary = null
      }
      return this.isClearActiveFlag
    },
    openActiveRowEvent (name, row) {
      switch (name) {
        case 'elxEditable1':
          if (this.permission !== 'SUB_BANK' && row.id !== localStorage.getItem('username')) {
            Message({ message: '您没有操作权限', type: 'warning' })
            return
          }
          break
        case 'elxEditable2':
          if (this.permission !== 'SUB_BANK' && row.staffid !== localStorage.getItem('username')) {
            Message({ message: '您没有操作权限', type: 'warning' })
            return
          }
          break
      }
      this.$nextTick(() => {
        let activeInfo = this.$refs[name].getActiveRow(row)
        //  正在编辑中
        if (activeInfo) {
          if (activeInfo.row === row || !this.$refs[name].checkValid().error) {
            if (activeInfo.isUpdate) {
              this.isClearActiveFlag = false
              MessageBox.confirm('检测到未保存的内容，是否在离开前保存修改?', '温馨提示', {
                closeOnClickModal: false,
                distinguishCancelAndClose: true,
                confirmButtonText: '保存',
                cancelButtonText: '放弃修改',
                type: 'warning'
              }).then(() => {
                this.$refs[name].setActiveRow(row)
                this.primary = row.id
                console.log(row.id)
                this.saveRowEvent(name, activeInfo.row)
              }).catch(action => {
                if (action === 'cancel') {
                  this.$refs[name].revert(activeInfo.row)
                  this.$refs[name].setActiveRow(row)
                  Message({ message: '放弃修改并离开当前行', type: 'warning' })
                } else {
                  Message({ message: '停留在当前行编辑', type: 'info' })
                }
              }).then(() => {
                this.isClearActiveFlag = true
              })
            } else {
              this.$refs[name].setActiveRow(row)
              this.primary = row.id
              console.log(row.id)
            }
          }
        } else {
          this.$refs[name].setActiveRow(row)
          this.primary = row.id
          console.log(row.id)
        }
      })
    },
    removeEvent (name, row) {
      if (this.permission !== 'SUB_BANK' && row.staffid !== localStorage.getItem('username')) {
        Message({ message: '您没有操作权限', type: 'warning' })
        return
      }
      switch (name) {
        case 'elxEditable1':
          this.$http.post(
            'http://' + document.domain + ':5000/staff',
            {
              type: 'Delete',
              primary: row.id
            },
            {
              emulateJSON: true
            }
          ).then(function (response) {
            if (parseInt(response.body.code) === 200) {
              this.$refs.elxEditable1.remove(row)
              Message({ message: '删除成功', type: 'success' })
            } else {
              Message({ message: '删除失败，有关联客户信息', type: 'warning' })
            }
          })
          break
        case 'elxEditable2':
          this.userLoading = true
          this.$http.post(
            'http://' + document.domain + ':5000/staffCustomer',
            {
              type: 'Delete',
              custid: row.id,
              staffid: row.staffid
            },
            {
              emulateJSON: true
            }
          ).then(function (response) {
            if (parseInt(response.body.code) === 200) {
              this.$refs.elxEditable2.remove(row)
              Message({ message: '删除成功', type: 'success' })
            } else {
              Message({ message: '删除失败', type: 'warning' })
            }
          })
          break
      }
    },
    saveRowEvent (name, row) {
      switch (name) {
        case 'elxEditable1':
          if (row.id === null || row.id === '') {
            Message({ message: '字段不能为空', type: 'warning' })
            return
          }
          break
        case 'elxEditable2':
          if (row.staffid === null || row.staffid === '') {
            Message({ message: '字段不能为空', type: 'warning' })
            return
          }
      }
      console.log(row)
      this.$refs[name].validateRow(row, valid => {
        if (valid && this.$refs[name].hasRowChange(row)) {
          switch (name) {
            case 'elxEditable1':
              this.$http.post(
                'http://' + document.domain + ':5000/staff',
                {
                  type: 'Update',
                  id: row.id,
                  name: row.name,
                  bank: row.bank,
                  dept: row.dept,
                  tel: row.tel,
                  addr: row.addr,
                  date_s: XEUtils.toDateString(row.date_s, 'yyyy-MM-dd'),
                  old_primary: this.primary
                },
                {
                  emulateJSON: true
                }
              ).then(function (response) {
                if (parseInt(response.body.code) === 200) {
                  //  更新合法
                  this.primary = null
                  this.$refs.elxEditable1.clearActive()
                  Message({ message: '保存成功', type: 'success' })
                  this.$refs.elxEditable1.reloadRow(row)
                } else if (parseInt(response.body.code) === 400) {
                  Message({ message: '新增记录失败，可能是身份证号重复', type: 'warning' })
                } else {
                  Message({ message: '保存失败\n' + response.body.msg, type: 'warning' })
                }
              })
              break
            case 'elxEditable2':
              this.$http.post(
                'http://' + document.domain + ':5000/staffCustomer',
                {
                  type: 'Update',
                  custID: row.id,
                  staffID: row.staffid,
                  serviceType: row.type,
                  old_custID: this.primary,
                  old_staffID: row.staffid
                },
                {
                  emulateJSON: true
                }
              ).then(function (response) {
                if (parseInt(response.body.code) === 200) {
                  //  更新合法
                  this.primary = null
                  this.$refs.elxEditable2.clearActive()
                  row.name = response.body.record.name
                  row.staffname = response.body.record.staffname
                  this.$refs.elxEditable2.reloadRow(row)
                  this.showDetail(this.detail)
                  Message({ message: '保存成功', type: 'success' })
                } else {
                  console.log(parseInt(response.body.code))
                  Message({ message: '保存失败', type: 'warning' })
                }
              })
              break
          }
        } else if (valid) {
          this.$refs[name].clearActive()
          this.primary = null
        }
      })
    },
    cancelRowEvent (name, row) {
      let activeInfo = this.$refs[name].getActiveRow()
      if (activeInfo && activeInfo.isUpdate) {
        this.isClearActiveFlag = false
        MessageBox.confirm('检测到未保存的内容，确定放弃修改?', '温馨提示', {
          closeOnClickModal: false,
          confirmButtonText: '放弃更改',
          cancelButtonText: '返回',
          type: 'warning'
        }).then(action => {
          if (action === 'confirm') {
            this.$refs[name].clearActive()
            this.$refs[name].revert(row)
            if (this.primary === null) {
              this.$refs[name].remove(row)
            }
            this.primary = null
          } else {
            this.$refs[name].setActiveRow(row)
          }
        }).catch(e => e).then(() => {
          this.isClearActiveFlag = true
        })
      } else {
        this.$refs[name].clearActive()
        this.primary = null
      }
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
