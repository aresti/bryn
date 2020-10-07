import { createApp } from "vue";
import TeamMemberApp from "./components/TeamMemberApp.vue";

import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const dashboardApp = createApp({
  delimiters: ["[[", "]]"],
  components: {
    "team-member-app": TeamMemberApp,
  },
  provide: {
    axios: axios,
  },
});

dashboardApp.mount("#team-app");
