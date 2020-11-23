<template>
  <section class="hero is-primary">
    <div class="hero-body">
      <header class="container">
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <h1 class="title">
                {{ team.name }}
              </h1>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
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
            </div>
          </div>
        </div>

        <h3 v-if="tenants.length === 1" class="subtitle">
          Tenant: {{ tenantName }}
        </h3>

        <base-dropdown-list
          v-if="tenants.length > 1"
          :title="tenantName"
          :items="tenants"
          :activeItem="tenant"
          @itemSelected="setActiveTenant"
          hoverable
        >
          <template v-slot:title>Tenant: {{ tenantName }}</template>
          <template v-slot:item="{ item: tenant }">
            {{ tenant.region.description }}
          </template>
        </base-dropdown-list>
      </header>
    </div>

    <div class="hero-foot">
      <dashboard-tabs />
    </div>
  </section>

  <main class="container mt-5">
    <router-view />
  </main>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

import DashboardTabs from "./DashboardTabs.vue";
import BaseDropdownList from "./BaseDropdownList.vue";
import BaseMessage from "./BaseMessage.vue";

export default {
  components: {
    DashboardTabs,
    BaseDropdownList,
    BaseMessage,
  },
  computed: {
    ...mapState(["user", "teams"]),
    ...mapGetters(["userFullName", "team", "tenant", "tenants", "tenantName"]),
  },
  methods: {
    ...mapActions(["setActiveTeam"]),
    onTeamSelect(team) {
      this.$router.push({
        name: "dashboard",
        params: { teamId: team.id },
      });
    },
    setActiveTab(key) {
      this.activeTab = key;
    },
  },
  beforeRouteUpdate(to, from) {
    // Update store activeTeam on route change
    if (to.params.teamId !== from.params.teamId) {
      const toTeam = this.teams.find(
        (team) => team.id === parseInt(to.params.teamId)
      );
      if (toTeam === undefined) {
        this.$router.push({
          name: "notfound",
          params: { pathMatch: to.path.split("/") },
        });
      }
      this.setActiveTeam(toTeam);
    }
  },
};
</script>