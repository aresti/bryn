<template>
  <aside class="menu">
    <the-dashboard-menu-list
      v-if="tenants.length"
      :routes="computeRoutes"
      label="Compute"
    />
    <the-dashboard-menu-list :routes="adminRoutes" label="Administration" />
  </aside>
</template>

<script>
import { mapGetters } from "vuex";
import TheDashboardMenuList from "@/components/TheDashboardMenuList";

export default {
  components: {
    TheDashboardMenuList,
  },

  data() {
    const dashboardRoutes = this.$router.options.routes.find(
      (route) => route.name === "dashboard"
    ).children;
    return {
      computeRoutes: dashboardRoutes.filter(
        (route) => route.meta.menuSection == "compute"
      ),
      adminRoutes: dashboardRoutes.filter(
        (route) => route.meta.menuSection == "admin"
      ),
    };
  },

  computed: mapGetters(["tenants"]),
};
</script>