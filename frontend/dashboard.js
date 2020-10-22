// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

// Mount DashboardApp
import { createApp } from "vue";
import DashboardApp from "./components/DashboardApp.vue";

const dashboardApp = createApp(DashboardApp);
dashboardApp.config.globalProperties.$http = axios;
dashboardApp.mount("#dashboardApp");
