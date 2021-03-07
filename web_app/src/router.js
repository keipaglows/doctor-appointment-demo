import Vue from "vue";
import Router from "vue-router";

import Appointments from "./views/Appointments.vue";

Vue.use(Router);

export default new Router({
  linkExactActiveClass: "active",
  routes: [
    {
      path: "/",
      name: "appointments",
      components: {
        default: Appointments
      }
    }
  ]
});
