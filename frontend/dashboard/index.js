import { createApp } from "vue";

import TeamMemberApp from "./components/TeamMemberApp.vue";

const dashboardApp = createApp({
  delimiters: ["[[", "]]"],
  components: {
    "team-member-app": TeamMemberApp,
  },
});

dashboardApp.mount("#team-app");
