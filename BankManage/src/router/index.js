import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import index from '@/views/Index.vue'
import register from '@/views/Register.vue'
import login from '@/views/Login'
import bank from '@/views/Bank'
import staff from '@/views/Staff'
import customer from '@/views/Customer'
import account from '@/views/account'
import loan from '@/views/Loan'
import summary from '@/views/Summary'
import error from '@/views/Error'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/register',
      name: 'Register',
      component: register
    },
    {
      path: '/index',
      name: 'Index',
      component: index
    },
    {
      path: '/',
      name: 'Login',
      component: login
    },
    {
      path: '/hello',
      name: 'Hello',
      component: HelloWorld
    },
    {
      path: '/bank',
      name: 'Bank',
      component: bank
    },
    {
      path: '/staff',
      name: 'Staff',
      component: staff
    },
    {
      path: '/customer',
      name: 'Customer',
      component: customer
    },
    {
      path: '/account',
      name: 'Account',
      component: account
    },
    {
      path: '/loan',
      name: 'Loan',
      component: loan
    },
    {
      path: '/summary',
      name: 'Summary',
      component: summary
    },
    {
      path: '*',
      name: 'Error',
      component: error
    }
  ]
})
