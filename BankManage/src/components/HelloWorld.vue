<template>
  <div class="hello">
    <h1>This is hello world page</h1>
    <h2>
      Click
      <router-link to="/">here</router-link>
      to see Home page
    </h2>
    <h2>
      Click
      <router-link to="/index">here</router-link>
      to see index page
    </h2>
    <h2>
      Click
      <router-link to="/login">here</router-link>
      to see login page
    </h2>
    <h2>
      Click
      <router-link to="/register">here</router-link>
      to see register page
    </h2>
    <h2>
      Click
      <router-link to="/bank">here</router-link>
      to see bank page
    </h2>
    <h2>
      Click
      <router-link to="/staff">here</router-link>
      to see staff page
    </h2>
    <h2>
      Click
      <router-link to="/customer">here</router-link>
      to see customer page
    </h2>
    <h2>
      Click
      <router-link to="/account">here</router-link>
      to see account page
    </h2>
    <h2>
      Click
      <router-link to="/loan">here</router-link>
      to see loan page
    </h2>
    <h2>
      Click
      <router-link to="/summary">here</router-link>
      to see summary page
    </h2>
    <h2>
      Click
      <router-link to="*">here</router-link>
      to see error page
    </h2>
    <h1>{{ msg }}</h1>
    <h2>Essential Links</h2>
    <ul>
      <li>
        <a
          href="https://vuejs.org"
          target="_blank"
        >
          Core Docs
        </a>
      </li>
      <li>
        <a
          href="https://forum.vuejs.org"
          target="_blank"
        >
          Forum
        </a>
      </li>
      <li>
        <a
          href="https://chat.vuejs.org"
          target="_blank"
        >
          Community Chat
        </a>
      </li>
      <li>
        <a
          href="https://twitter.com/vuejs"
          target="_blank"
        >
          Twitter
        </a>
      </li>
      <br>
      <li>
        <a
          href="http://vuejs-templates.github.io/webpack/"
          target="_blank"
        >
          Docs for This Template
        </a>
      </li>
    </ul>
    <h2>Ecosystem</h2>
    <ul>
      <li>
        <a
          href="http://router.vuejs.org/"
          target="_blank"
        >
          vue-router
        </a>
      </li>
      <li>
        <a
          href="http://vuex.vuejs.org/"
          target="_blank"
        >
          vuex
        </a>
      </li>
      <li>
        <a
          href="http://vue-loader.vuejs.org/"
          target="_blank"
        >
          vue-loader
        </a>
      </li>
      <li>
        <a
          href="https://github.com/vuejs/awesome-vue"
          target="_blank"
        >
          awesome-vue
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
