<template>
  <div
    class="page-content is-flex is-flex-direction-column is-align-items-stretch is-flex-grow-1"
  >
    <the-dashboard-header />

    <section class="section is-flex is-flex-grow-1">
      <base-flex-centered v-if="teamErroredOnGet">
        <base-message color="danger" light>
          We couldn't fetch your team data. There may be a temporary issue on
          our end. Please try again shortly.
        </base-message>
      </base-flex-centered>

      <base-flex-centered v-if="allTenantsErroredOnGet">
        <base-message color="danger" light>
          All of your tenants were unreachable, there may be a temporary issue
          on our end. Please try again shortly.
        </base-message>
      </base-flex-centered>

      <base-flex-centered v-else-if="loading">
        <div class="loader is-loading"></div>
      </base-flex-centered>

      <div v-else class="container">
        <div class="columns is-variable is-6">
          <div class="column is-one-fifth">
            <the-dashboard-menu />
          </div>
          <div class="column is-four-fiths">
            <the-dashboard-content />
          </div>
        </div>
      </div>
    </section>
  </div>

  <the-footer class="mt-5" />
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

import TheDashboardContent from "@/components/TheDashboardContent";
import TheDashboardHeader from "@/components/TheDashboardHeader";
import TheDashboardMenu from "@/components/TheDashboardMenu";
import TheFooter from "@/components/TheFooter";

export default {
  // Template dependencies
  components: {
    TheDashboardContent,
    TheDashboardHeader,
    TheDashboardMenu,
    TheFooter,
  },

  // Composition
  inject: ["toast"],

  // Local state
  data() {
    return {
      teamErroredOnGet: false,
      allTenantsErroredOnGet: false,
    };
  },

  computed: {
    ...mapState(["teams", "user"]),
    ...mapGetters([
      "loading",
      "team",
      "tenants",
      "getTenantById",
      "getRegionById",
    ]),
  },

  // Events
  watch: {
    async team(_newTeam, _oldTeam) {
      this.getTeamData();
      if (this.tenants.length) {
        this.getTenantData();
      }
    },
  },

  created() {
    /* Set activeTeamId for initial route */
    this.setTeamForRoute(this.$route);
  },

  beforeRouteUpdate(to, from) {
    /* Update activeTeamId on route change (since Vue component instance is reused) */
    if (to.params.teamId !== from.params.teamId) {
      this.setTeamForRoute(to);
    }
  },

  // Non-reactive
  methods: {
    ...mapActions([
      "setActiveTeam",
      "fetchTeamSpecificData",
      "fetchAllTenantData",
    ]),

    setTeamForRoute(route) {
      /* Set the activeTeamId state from route params */
      const toTeam = this.teams.find(
        (team) => team.id === parseInt(route.params.teamId)
      );
      if (toTeam === undefined) {
        this.$router.push({
          name: "notfound",
          params: { pathMatch: route.path.split("/") },
        });
      }
      this.setActiveTeam(toTeam);
    },

    async getTeamData() {
      /* Fetch data for the active team */
      this.teamErroredOnGet = false;
      try {
        await this.fetchTeamSpecificData();
      } catch (err) {
        this.teamErroredOnGet = true;
        this.toast.error(err.toString());
      }
    },

    async getTenantData() {
      /* Fetch data for all of the active team's tenants */
      this.allTenantsErroredOnGet = false;
      try {
        const results = await this.fetchAllTenantData();
        /*
         * Result is per-tenant, from Promise.allSettled
         * Trigger toasts for errors
         */
        results
          .filter((result) => result.status == "rejected")
          .map((result) => {
            this.toast.error(result.reason.message);
          });

        // Set dashboard state
        this.allTenantsErroredOnGet = results.every(
          (result) => result.status == "rejected"
        );
      } catch (err) {
        // Unexpected error
        this.allTenantsErroredOnGet = true;
        this.toast.error(err.toString());
      }
    },
  },
};
</script>

<style scoped>
.loader {
  height: 200px;
  width: 200px;
}
</style>