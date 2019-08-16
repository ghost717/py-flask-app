import Vue from 'vue';
import Router from 'vue-router';

import Posts from './components/Posts.vue';

import Login from './components/Login';
import Register from './components/Register';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/posts',
      name: 'Posts',
      component: Posts,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
  ],
});
