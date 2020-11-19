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
                title="Select team"
                :items="teams"
                :activeItem="team"
                @itemSelected="setActiveTeam"
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
      <dashboard-tabs
        :tabs="tabs"
        :activeTab="activeTab"
        @tabSelected="setActiveTab"
      />
    </div>
  </section>

  <main class="container mt-5">
    <base-message v-if="!tenant" color="danger">
      This team has no active tenants. Please contact the CLIMB administrator.
    </base-message>
    <keep-alive v-else>
      <component v-bind:is="activeTabComponent" :team="team" :tenant="tenant" />
    </keep-alive>
  </main>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

import DashboardTabs from "./DashboardTabs.vue";
import TabServers from "./TabServers.vue";
import TabVolumes from "./TabVolumes.vue";
import TabSshKeys from "./TabSshKeys.vue";
import TabTeam from "./TabTeam.vue";
import TabUserProfile from "./TabUserProfile.vue";
import TabLicense from "./TabLicense.vue";
import BaseDropdownList from "./BaseDropdownList.vue";
import BaseMessage from "./BaseMessage.vue";

export default {
  components: {
    DashboardTabs,
    TabServers,
    TabVolumes,
    TabSshKeys,
    TabTeam,
    TabUserProfile,
    TabLicense,
    BaseDropdownList,
    BaseMessage,
  },
  data() {
    return {
      tabs: {
        servers: "Servers",
        volumes: "Volumes",
        "ssh-keys": "SSH Keys",
        team: "Team Info",
        "user-profile": "User Profile",
        license: "License",
      },
      activeTab: "servers",
    };
  },
  computed: {
    ...mapState(["user", "teams"]),
    ...mapGetters(["userFullName", "team", "tenant", "tenants", "tenantName"]),
    activeTabComponent() {
      return "tab-" + this.activeTab;
    },
  },
  methods: {
    ...mapActions(["setActiveTeam"]),
    setActiveTab(key) {
      this.activeTab = key;
    },
  },
  beforeMount() {
    this.$store.dispatch("initStore");
  },
};
</script>