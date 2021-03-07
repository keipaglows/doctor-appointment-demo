import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    doctor: null,
    office: null
  },
  mutations: {
    setDoctor(state, doctor) {
      state.doctor = doctor
    },
    setOffice(state, office) {
      state.office = office
    }
  },
  actions: {
  },
  modules: {
  }
})
