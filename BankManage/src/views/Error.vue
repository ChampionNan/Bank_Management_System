<template>
  <html>
    <h1 class="title">您要查看的页面不存在或已删除</h1>
    <h2 class="subtitle">点击图片返回首页</h2>
    <a href="/"><img src="static/4042.jpg"></a>
  </html>
</template>

<script>
//  import { MessageBox, Message } from 'element-ui'
export default {
  name: 'Error',
  methods: {
    f () {
      this.$message({
        message: 'hello'
      })
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
  .subtitle {
    text-align: center;
    color: #606266;
    font-size: 16px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
</style>
