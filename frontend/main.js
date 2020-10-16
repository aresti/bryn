require("./assets/sass/main.scss");

/* Hamburgers */
document.addEventListener("DOMContentLoaded", () => {
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll(".navbar-burger"),
    0
  );
  if ($navbarBurgers.length > 0) {
    $navbarBurgers.forEach((el) => {
      el.addEventListener("click", () => {
        const target = el.dataset.target;
        const $target = document.getElementById(target);
        el.classList.toggle("is-active");
        $target.classList.toggle("is-active");
      });
    });
  }
});

/* Vue dashboard app */

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
