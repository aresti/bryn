import { createApp } from "vue";
import Toast, { POSITION } from "vue-toastification";
import "vue-toastification/dist/index.css";
import VueClickAway from "vue3-click-away";
import { axios } from "@/api";
import store from "@/store";
import router from "@/router";

import App from "@/App";

const app = createApp(App);

app.use(store);
app.use(router);
app.config.globalProperties.$http = axios;
app.use(VueClickAway);

const toastOptions = {
  position: POSITION.BOTTOM_LEFT,
};
app.use(Toast, toastOptions);

app.mount("#dashboardApp");
