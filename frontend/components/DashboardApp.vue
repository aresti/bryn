<template>
  <section class="hero is-primary">
    <div class="hero-body">
      <header class="container">
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <h1 class="title">
                {{ activeTeam.name }}
              </h1>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <base-dropdown-list
                title="Select team"
                :items="teams"
                :activeItem="activeTeam"
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
          Tenant: {{ activeTenantName }}
        </h3>

        <base-dropdown-list
          v-if="tenants.length > 1"
          :title="activeTenantName"
          :items="tenants"
          :activeItem="activeTenant"
          @itemSelected="setActiveTenant"
          hoverable
        >
          <template v-slot:title>Tenant: {{ activeTenantName }}</template>
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
    <base-message v-if="!activeTenant" color="danger">
      This team has no active tenants. Please contact the CLIMB administrator.
    </base-message>
    <keep-alive>
      <component
        v-bind:is="activeTabComponent"
        :team="activeTeam"
        :tenant="activeTenant"
      />
    </keep-alive>
  </main>
</template>

<script>
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
      teams: [],
      teamsDataId: "teamsData",
      activeTeam: null,
      activeTenant: null,
      user: null,
      userDataId: "userData",
      flavors: [],
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
    userFullName() {
      return `${this.user.first_name} ${this.user.last_name}`;
    },
    activeTabComponent() {
      return "tab-" + this.activeTab;
    },
    tenants() {
      if (this.activeTeam) {
        return this.activeTeam.tenants;
      } else {
        return [];
      }
    },
    activeTenantName() {
      return this.activeTenant.region.description;
    },
  },
  methods: {
    getTeams() {
      this.teams = JSON.parse(
        document.getElementById(this.teamsDataId).textContent
      );
      this.setActiveTeam(this.teams[0]);
    },
    getDefaultTenant(team) {
      if (!team.tenants.length) return null;
      if (!team.default_region) return self.tenants[0];
      for (let tenant of team.tenants) {
        if (tenant.region.id === team.default_region) return tenant;
      }
    },
    getUser() {
      this.user = JSON.parse(
        document.getElementById(this.userDataId).textContent
      );
    },
    setActiveTeam(team) {
      this.activeTeam = team;
      this.setActiveTenant(this.getDefaultTenant(team));
    },
    setActiveTenant(tenant) {
      this.activeTenant = tenant;
      // TODO: api call to update default region for team, if changed
    },
    setActiveTab(key) {
      this.activeTab = key;
    },
  },
  beforeMount() {
    this.getTeams();
    this.getUser();
  },
};
</script>