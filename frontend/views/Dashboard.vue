<template>
  <div
    class="page-content is-flex is-flex-direction-column is-align-items-stretch is-flex-grow-1"
  >
    <section class="hero is-primary">
      <div class="hero-body">
        <header class="container">
          <base-level>
            <template v-slot:left>
              <base-level-item>
                <h1 class="title">
                  {{ team.name }}
                </h1>
              </base-level-item>
            </template>
            <template v-slot:right>
              <base-level-item>
                <base-dropdown-list
                  @itemSelected="onTeamSelect"
                  title="Select team"
                  :items="teams"
                  :activeItem="team"
                  hoverable
                  right
                >
                  <template v-slot:title>Switch team</template>
                  <template v-slot:item="{ item: team }">
                    {{ team.name }}
                  </template>
                </base-dropdown-list>
              </base-level-item>
            </template>
          </base-level>
          <h2 class="subtitle">
            {{ userFullName }}
          </h2>
        </header>
      </div>

      <div class="hero-foot">
        <dashboard-tabs v-if="!loading && !erroredOnGet" />
      </div>
    </section>

    <section class="section is-flex is-flex-grow-1">
      <base-flex-centered v-if="erroredOnGet">
        <base-notification color="danger" light>
          All of your tenants were unreachable. Please check your network
          connection.
        </base-notification>
      </base-flex-centered>

      <base-flex-centered v-else-if="loading">
        <div class="loader is-loading"></div>
      </base-flex-centered>

      <router-view v-else v-slot="{ Component, route }">
        <transition name="fade" mode="out-in">
          <keep-alive>
            <component
              :is="Component"
              class="container"
              :class="'tab-' + route.name"
            />
          </keep-alive>
        </transition>
      </router-view>
    </section>
  </div>

  <the-footer class="mt-5" />
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import { useToast } from "vue-toastification";

import BaseDropdownList from "@/components/BaseDropdownList";
import BaseFlexCentered from "@/components/BaseFlexCentered";
import BaseLevel from "@/components/BaseLevel";
import BaseLevelItem from "@/components/BaseLevelItem";
import BaseNotification from "@/components/BaseNotification";
import DashboardTabs from "@/components/DashboardTabs";
import TheFooter from "@/components/TheFooter";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },
  components: {
    BaseDropdownList,
    BaseFlexCentered,
    BaseLevel,
    BaseLevelItem,
    BaseNotification,
    DashboardTabs,
    TheFooter,
  },
  data() {
    return {
      loading: false,
      erroredOnGet: false,
    };
  },
  computed: {
    ...mapState(["teams", "user"]),
    ...mapGetters([
      "userFullName",
      "team",
      "tenants",
      "getTenantById",
      "getRegionById",
    ]),
  },
  methods: {
    ...mapActions(["setActiveTeam", "getAllTeamData"]),
    setTeamForRoute(route) {
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
    onTeamSelect(team) {
      this.$router.push({
        name: this.$route.name,
        params: { teamId: team.id },
      });
    },
    async getTeamInstances() {
      try {
        await this.$store.dispatch("instances/getTeamInstances");
      } catch (err) {
        this.toast.error(`Error fetching team instances: ${err.message}`);
      }
    },
  },
  watch: {
    async team(_newTeam, _oldTeam) {
      // Team has been set, fetch data for all tenants
      this.erroredOnGet = false;
      this.loading = true;
      const results = await this.getAllTeamData();
      results
        .filter((result) => result.status == "rejected")
        .map((result) => {
          this.toast.error(result.reason.message);
        });
      this.erroredOnGet = results.every(
        (result) => result.status == "rejected"
      );
      this.loading = false;
    },
  },
  created() {
    // Set activeTeam for initial route
    this.setTeamForRoute(this.$route);
  },
  beforeRouteUpdate(to, from) {
    // Update activeTeam on route change (since Vue component instance is reused)
    if (to.params.teamId !== from.params.teamId) {
      this.setTeamForRoute(to);
    }
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.loader {
  height: 200px;
  width: 200px;
}

.hero {
  background: rgb(32, 60, 71);
  background: linear-gradient(
    0deg,
    rgba(32, 60, 71, 1) 0%,
    rgba(38, 70, 83, 1) 100%
  );
}
</style>