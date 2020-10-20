/* Vue dashboard app */

import { createApp } from "vue";
import DashboardApp from "./components/DashboardApp.vue";

import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const dashboardApp = createApp({
  delimiters: ["<%", "%>"],
  components: {
    DashboardApp,
  },
  provide: {
    axios: axios,
  },
  template: "<DashboardApp/>",
});

dashboardApp.mount("#dashboardApp");
