<template>
  <div class="hero-foot">
    <nav class="tabs is-boxed is-fullwidth">
      <div class="container">
        <ul>
          <router-link
            v-for="route in teamRoutes"
            :key="route.path"
            :to="route.path"
            custom
            v-slot="{ href, navigate, isExactActive }"
          >
            <li :class="{ 'is-active has-text-primary': isExactActive }">
              <a :href="href" @click="navigate">{{
                route.meta.displayNameShort
              }}</a>
            </li>
          </router-link>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { TENANTS } from "@/store/getter-types";

export default {
  computed: {
    ...mapGetters({
      tenants: TENANTS,
    }),

    teamRoutes() {
      const touchRoutes = this.$router.options.routes
        .find((route) => route.name === "teamHome")
        .children.filter((route) => route.name !== "dashboard");
      if (this.tenants.length === 0) {
        return touchRoutes.filter(
          (route) => route.meta.menuSection !== "compute"
        );
      } else {
        return touchRoutes;
      }
    },
  },
};
</script>