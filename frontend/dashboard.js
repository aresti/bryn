import { createApp } from "vue";
import { axios } from "@/api";
import store from "@/store";
import router from "@/router";

import App from "@/App";

const dashboardApp = createApp(App);
dashboardApp.use(store);
dashboardApp.use(router);
dashboardApp.config.globalProperties.$http = axios;

dashboardApp.mount("#dashboardApp");
