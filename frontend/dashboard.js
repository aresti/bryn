/* Vue dashboard app */

import { createApp } from "vue";
import DashboardApp from "./components/DashboardApp.vue";

// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const dashboardApp = createApp({
  delimiters: ["<%", "%>"],
  components: {
    DashboardApp,
  },
  template: "<DashboardApp/>",
});

dashboardApp.config.globalProperties.$http = axios;

dashboardApp.mount("#dashboardApp");
