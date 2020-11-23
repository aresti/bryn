<template>
  <nav class="tabs is-boxed is-fullwidth">
    <div class="container">
      <ul>
        <router-link
          v-for="route in tabRoutes"
          :key="route.path"
          :to="route.path"
          custom
          v-slot="{ href, navigate, isExactActive }"
        >
          <li :class="{ 'is-active': isExactActive }">
            <a :href="href" @click="navigate">{{ route.meta.displayName }}</a>
          </li>
        </router-link>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    const dashboardRoute = this.$router.options.routes.find(
      (route) => route.name === "dashboard"
    );
    return {
      tabRoutes: dashboardRoute.children.filter((route) => route.meta.showTab),
    };
  },
  computed: {
    currentRoute() {
      return this.$route;
    },
  },
};
</script>