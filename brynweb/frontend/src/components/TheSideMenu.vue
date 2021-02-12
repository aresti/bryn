<template>
  <aside class="menu">
    <the-side-menu-list :routes="generalRoutes" label="General" />
    <the-side-menu-list
      v-if="tenants.length"
      :routes="computeRoutes"
      label="Compute"
    />
    <the-side-menu-list :routes="adminRoutes" label="Administration" />
  </aside>
</template>

<script>
import { mapGetters } from "vuex";
import TheSideMenuList from "@/components/TheSideMenuList";

export default {
  components: {
    TheSideMenuList,
  },

  data() {
    const teamRoutes = this.$router.options.routes.find(
      (route) => route.name === "teamHome"
    ).children;
    return {
      generalRoutes: teamRoutes.filter(
        (route) => route.meta.menuSection == "general"
      ),
      computeRoutes: teamRoutes.filter(
        (route) => route.meta.menuSection == "compute"
      ),
      adminRoutes: teamRoutes.filter(
        (route) => route.meta.menuSection == "admin"
      ),
    };
  },

  computed: mapGetters(["tenants"]),
};
</script>