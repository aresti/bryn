import { createRouter, createWebHashHistory } from "vue-router";

import Dashboard from "@/components/Dashboard.vue";
import NotFound from "@/components/NotFound.vue";
import Servers from "@/components/Servers.vue";
import Volumes from "@/components/Volumes.vue";
import SSHKeys from "@/components/SSHKeys.vue";
import Team from "@/components/Team.vue";
import UserProfile from "@/components/UserProfile.vue";
import Licence from "@/components/Licence.vue";

const routes = [
  {
    path: "/dashboard/:teamId",
    name: "dashboard",
    component: Dashboard,
    children: [
      {
        path: "servers",
        name: "servers",
        component: Servers,
        meta: { displayName: "Servers", showTab: true },
      },
      {
        path: "volumes",
        name: "volumes",
        component: Volumes,
        meta: { displayName: "Volumes", showTab: true },
      },
      {
        path: "sshkeys",
        name: "sshkeys",
        component: SSHKeys,
        meta: { displayName: "SSH Keys", showTab: true },
      },
      {
        path: "team",
        name: "team",
        component: Team,
        meta: { displayName: "Team Profile", showTab: true },
      },
      {
        path: "user",
        name: "userProfile",
        component: UserProfile,
        meta: { displayName: "User Profile", showTab: true },
      },
      {
        path: "licence",
        name: "licence",
        component: Licence,
        meta: { displayName: "Licence", showTab: true },
      },
    ],
    redirect: { name: "servers" },
  },
  { path: "/:pathMatch(.*)*", name: "notfound", component: NotFound },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
