import { createRouter, createWebHashHistory } from "vue-router";

import Home from "@/views/Home";
import Dashboard from "@/views/Dashboard";
import NotFound from "@/views/NotFound";
import Servers from "@/views/Servers";
import Volumes from "@/views/Volumes";
import SSHKeys from "@/views/SSHKeys";
import Team from "@/views/Team";
import UserProfile from "@/views/UserProfile";
import Licence from "@/views/Licence";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/dashboard/:teamId",
    name: "dashboard",
    component: Dashboard,
    redirect: (to) => {
      return to.path + "/servers";
    },
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
  },
  { path: "/:pathMatch(.*)*", name: "notfound", component: NotFound },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
