import actions from './store/actions'
import state from './store/state'
import mutations from './store/mutations'
import getters from './store/getters'

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// Create a new store
const store = new Vuex.Store({
  actions: actions,
  getters: getters,
  mutations: mutations,
  state: state
})

export default store;