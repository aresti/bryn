import { createRouter, createWebHashHistory } from "vue-router";
import Dashboard from "@/components/Dashboard.vue";
import NotFound from "@/components/NotFound.vue";

const routes = [
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
  { path: "/team/:teamId", name: "Dashboard", component: Dashboard },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
