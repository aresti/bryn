<template>
  <div
    class="page-content pb-5 is-flex is-flex-direction-column is-align-items-stretch is-flex-grow-1"
  >
    <the-header />

    <section class="section is-flex is-flex-grow-1">
      <base-flex-centered v-if="teamErroredOnGet">
        <base-message color="danger" light>
          We couldn't fetch your team data. There may be a temporary issue on
          our end. Please try again shortly.
        </base-message>
      </base-flex-centered>

      <base-flex-centered v-else-if="allTenantsErroredOnGet">
        <base-message color="danger" light>
          All of your tenants were unreachable, there may be a temporary issue
          on our end. Please try again shortly.
        </base-message>
      </base-flex-centered>

      <base-flex-centered v-else-if="!ready">
        <div class="loader is-loading"></div>
      </base-flex-centered>

      <div v-else class="container">
        <div class="columns is-variable is-6">
          <div class="column is-one-fifth is-hidden-touch">
            <the-side-menu />
          </div>
          <div class="column">
            <the-content />
          </div>
        </div>
      </div>
    </section>
  </div>

  <the-footer />
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";
import {
  FETCH_ALL_TENANT_DATA,
  FETCH_TEAM_SPECIFIC_DATA,
  SET_ACTIVE_TEAM,
} from "@/store/action-types";
import {
  GET_REGION_BY_ID,
  GET_TENANT_BY_ID,
  TEAM,
  TENANTS,
} from "@/store/getter-types";
import { SET_TEAM_INITIALIZED } from "@/store/mutation-types";

import TheContent from "@/components/TheContent";
import TheHeader from "@/components/TheHeader";
import TheSideMenu from "@/components/TheSideMenu";
import TheFooter from "@/components/TheFooter";

export default {
  // Template dependencies
  components: {
    TheContent,
    TheHeader,
    TheSideMenu,
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
    ...mapState({
      ready: (state) => state.ready,
      teams: (state) => state.teams,
      user: (state) => state.user,
    }),
    ...mapGetters({
      getRegionId: GET_REGION_BY_ID,
      getTenantById: GET_TENANT_BY_ID,
      team: TEAM,
      tenants: TENANTS,
    }),
  },

  // Events
  watch: {
    async team() {
      await this.getTeamData();
      if (this.tenants.length) {
        await this.getAllTenantData();
      }
      this.setTeamInitialized(this.team);
    },

    ready: {
      handler(ready) {
        if (ready) {
          this.setTeamForRoute(this.$route);
        }
      },
      immediate: true,
    },
  },

  beforeRouteUpdate(to, from) {
    if (to.params.teamId !== from.params.teamId) {
      // Update activeTeamId on route change (since Vue component instance is reused)
      this.setTeamForRoute(to);
    }
    if (to.meta.menuSection === "compute") {
      const hasTenants = this.tenants.length;
      const hasLicense = this.team.licenceIsValid;
      if (!(hasTenants && hasLicense)) {
        // No tenants or no license, redirect to team admin view
        this.$router.push({
          name: "dashboard",
          params: { teamId: to.params.teamId },
        });
      }
    }
  },

  // Non-reactive
  methods: {
    ...mapActions({
      fetchAllTenantData: FETCH_ALL_TENANT_DATA,
      fetchTeamSpecificData: FETCH_TEAM_SPECIFIC_DATA,
      setActiveTeam: SET_ACTIVE_TEAM,
    }),

    ...mapMutations({
      setTeamInitialized: SET_TEAM_INITIALIZED,
    }),

    setTeamForRoute(route) {
      /* Set the activeTeamId state from route params */
      const toTeam = this.teams.find((team) => team.id === route.params.teamId);
      if (toTeam === undefined) {
        this.$router.push({
          name: "notfound",
          params: { pathMatch: route.path.split("/").slice(1) },
        });
      }
      this.setActiveTeam(toTeam);
    },

    async getTeamData() {
      /* Fetch data for the active team */
      this.teamErroredOnGet = false;
      try {
        await this.fetchTeamSpecificData(this.team);
      } catch (err) {
        this.teamErroredOnGet = true;
        this.toast.error(err.toString());
      }
    },

    async getAllTenantData() {
      /* Fetch data for all of the active team's tenants */
      this.allTenantsErroredOnGet = false;
      try {
        const results = await this.fetchAllTenantData(this.team);
        /*
         * Result is per-tenant, from Promise.allSettled
         * Trigger toasts for errors
         */
        results
          .filter((result) => result.status == "rejected")
          .map((result) => {
            this.toast.error(result.reason.message);
          });

        // Set state
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
.container {
  max-width: 100%;
}

.loader {
  height: 200px;
  width: 200px;
}
</style>