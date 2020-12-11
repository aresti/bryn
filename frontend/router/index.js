import { createRouter, createWebHashHistory } from "vue-router";

import Home from "@/views/Home";
import Dashboard from "@/views/Dashboard";
import NotFound from "@/views/NotFound";
import Servers from "@/views/Servers";
import Volumes from "@/views/Volumes";
import KeyPairs from "@/views/KeyPairs";
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
        meta: { displayName: "Servers", menuSection: "compute" },
      },
      {
        path: "volumes",
        name: "volumes",
        component: Volumes,
        meta: { displayName: "Volumes", menuSection: "compute" },
      },
      {
        path: "keypairs",
        name: "keypairs",
        component: KeyPairs,
        meta: { displayName: "SSH Keys", menuSection: "compute" },
      },
      {
        path: "team",
        name: "team",
        component: Team,
        meta: { displayName: "Team Management", menuSection: "admin" },
      },
      {
        path: "user",
        name: "userProfile",
        component: UserProfile,
        meta: { displayName: "User Profile", menuSection: "admin" },
      },
      // {
      //   path: "licence",
      //   name: "licence",
      //   component: Licence,
      //   meta: { displayName: "Licence", menuSection: "admin" },
      // },
    ],
  },
  { path: "/:pathMatch(.*)*", name: "notfound", component: NotFound },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
