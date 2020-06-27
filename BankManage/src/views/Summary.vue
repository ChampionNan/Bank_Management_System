<template>
  <div v-loading="loading">
    <el-row>
      <el-col :span="24">
        <div class="title">业务统计</div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        <div class="subtitle">1.统计条件</div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        开始时间<el-input type="month" min="0" v-model="lowerBound" placeholder="开始时间" aria-required="true"></el-input>
      </el-col>
      <el-col :span="4">
        停止时间<el-input type="month" min="0" v-model="upperBound" placeholder="停止时间"></el-input>
      </el-col>
      <el-col :span="4">
        时间粒度<el-select v-model="timegrain" placeholder="month">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-col>
      <el-col :span="4">
        业务分类<el-select v-model="sumtype" placeholder="all">
          <el-option v-for="item in classtype" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-col>
      <el-col :span="4">
        统计项目<el-select v-model="datatype" placeholder="datatype">
          <el-option v-for="item in statistics" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-col>
      <el-col :span="2">
        <el-button type="primary" @click="start" style="margin-top: 20px;">提交</el-button>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4">
        <div class="subtitle">2.统计表</div>
      </el-col>
    </el-row>
    <elx-editable ref="elxEditable1" size="small" class="table" border :data.sync="userList" :edit-config="{ trigger: 'manual', mode: 'row' }" style="width: 100%">
      <elx-editable-column prop="time" label="时间"></elx-editable-column>
      <template v-for="item in columnConfigs">
        <template v-if="item._show">
          <elx-editable-column v-bind="item" :key="item.prop"></elx-editable-column>
        </template>
      </template>
    </elx-editable>
    <el-row :gutter="20">
      <el-col :span="4">
        <div class="subtitle" style="margin-top: 20px;">3.统计图</div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="4">
        <el-radio v-model="graphtype" label="curve">按时间统计</el-radio>
        <el-radio v-model="graphtype" label="pie">按支行统计</el-radio>
      </el-col>
    </el-row>
    <div align="center">
      <ve-pie :data="chartData" v-if="graphtype == 'pie'" width="800px"></ve-pie>
      <ve-line :data="chartData2" :settings="charSettings" width="800px" v-else></ve-line>
    </div>
  </div>
</template>

<script>
import XEUtils from 'xe-utils'
//  import XEAjax from 'xe-ajax'
import { Message } from 'element-ui'
export default {
  data () {
    return {
      options: [{
        value: 'month',
        label: '月'
      }, {
        value: 'season',
        label: '季'
      }, {
        value: 'year',
        label: '年'
      }],
      classtype: [{
        value: 'saving',
        label: '储蓄业务'
      }, {
        value: 'loan',
        label: '贷款业务'
      }],
      statistics: [{
        value: 'money',
        label: '业务总金额'
      }, {
        value: 'user',
        label: '用户数'
      }],
      loading: false,
      showpie: false,
      charSettings: {},
      list: [],
      result: false,
      isClearActiveFlag: true,
      chartData: {
        columns: [],
        rows: []
      },
      chartData2: {
        columns: [],
        rows: []
      },
      columnConfigs: [],
      userList: [],
      upperBound: '2019-06',
      lowerBound: '2015-01',
      timegrain: '',
      sumtype: '',
      datatype: '',
      graphtype: '',
      permission: ''
    }
  },
  created () {
    this.permission = localStorage.getItem('type')
    if (this.permission !== 'SUB_BANK') {
      //  this.push('/404')
    }
    this.timegrain = 'month'
    this.sumtype = 'saving'
    this.datatype = 'money'
    this.graphtype = 'curve'
  },
  methods: {
    start: function () {
      if (this.upperBound === '' || this.lowerBound === '') {
        Message({ message: '时间范围不能为空', type: 'warning' })
        return
      }
      this.$http.post(
        'http://' + document.domain + ':5000/summary',
        {
          upperBound: XEUtils.toDateString(this.upperBound, 'yyyy-MM-dd'),
          lowerBound: XEUtils.toDateString(this.lowerBound, 'yyyy-MM-dd'),
          timegrain: this.timegrain,
          sumtype: this.sumtype,
          datatype: this.datatype,
          graphtype: 'curve'
        },
        {
          emulateJSON: true
        }
      ).then(function (response) {
        if (parseInt(response.body.code) === 200) {
          this.columnConfigs = []
          this.result = true
          let tempList = response.body.columnList
          tempList.forEach(column => {
            let item = {
              prop: column,
              label: column,
              _show: true
            }
            this.columnConfigs.push(item)
          })
          this.userList = response.body.rawData
          this.cleanData(response.body.columnList, response.body.rawData)
          this.makeLineChart(response.body.columnList, response.body.rawData)
          this.makePieChart(response.body.columnList, response.body.sumdata)
          Message({ message: '查询成功', type: 'success' })
        } else {
          this.result = false
          Message({ message: '查询结果为空', type: 'warning' })
        }
      })
    },
    cleanData: function (columnList, rawData) {
      for (var i = 0; i < rawData.length; i++) {
        for (var j = 0; j < columnList.length; j++) {
          if (rawData[i][columnList[j]] === null) {
            rawData[i][columnList[j]] = 0
          }
        }
      }
      for (i = 0; i < rawData.length; i++) {
        if (rawData[i].time.indexOf('.') !== -1) {
          XEUtils.toDateString(rawData[i], 'yyyy.mm')
        }
      }
      for (i = 0; i < rawData.length; i++) {
        for (j = i + 1; j < rawData.length; j++) {
          if (rawData[i].time > rawData[j].time) {
            var temp = rawData[i]
            rawData[i] = rawData[j]
            rawData[j] = temp
          }
        }
      }
    },
    makePieChart: function (columnList, rawData) {
      console.log('makePieChart')
      this.chartData.rows = []
      //  console.log(rawData)
      
      this.chartData.columns = ['SUB_BANK', 'AMOUNT']
      this.chartData.rows = rawData
      /*
      for (var i = 0; i < columnList.length; i++) {
        this.chartData.rows.push({ 支行: columnList[i], index: 0 })
      }
      console.log(this.chartData.rows)
      for (i = 0; i < rawData.length; i++) {
        for (var j = 0; j < columnList.length; j++) {
          this.chartData.rows[j].index += rawData[i][columnList[j]]
        }
      }
      console.log(this.chartData)*/
    },
    makeLineChart: function (columnList, rawData) {
      console.log('makeLineChart')
      this.chartData2.columns = []
      this.chartData2.rows = []
      this.chartData2.columns = ['time']
      for (var i = 0; i < columnList.length; i++) {
        this.chartData2.columns.push(columnList[i])
        console.log(columnList[i])
      }
      console.log(this.chartData2)
      this.chartData2.rows = rawData
      this.charSettings = {
        metrics: columnList,
        dimension: ['time'],
        min: ['dataMin', 'dataMin'],
        max: ['dataMax', 'dataMax']
      }
      console.log(this.chartData2)
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
