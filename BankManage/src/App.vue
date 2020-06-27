<template>
  <div id="app">
    <div class="body">
      <router-view/>
    </div>
    <footer class="footer">
      <p>
        USTC DATABASE LAB 2020-spring
      </p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  position: relative;
  min-height: 100% ;
}
.footer {
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  font-size: 14px;
  color: grey;
  text-align: center;
  width: 100%; /*展开footer宽度*/
  position: absolute;
  height: 100px;
}
</style>
