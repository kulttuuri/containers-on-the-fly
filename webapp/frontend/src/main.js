import Vue from 'vue'
import App from './App.vue'
import router from './router'
//import store from './store'
import vuetify from './plugins/vuetify'
import AppSettings from '/src/AppSettings.js';
import '/src/main.css';

import { store } from './store';

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  beforeCreate() { this.$store.commit('initialiseStore'); },
  render: h => h(App)
}).$mount('#app')

// Mixins
Vue.mixin({
  computed: {
    AppSettings() {
      return AppSettings;
    }
  }
})