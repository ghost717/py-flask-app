import Vue from 'vue';
import Router from 'vue-router';

import Posts from './components/Posts.vue';

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
  ],
});
