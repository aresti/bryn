<template>
  <section class="hero is-primary">
    <div class="hero-body">
      <header class="container">
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <h1 class="title">
                {{ currentTeam.name }}
              </h1>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <team-selector
                :teams="teams"
                :currentTeam="currentTeam"
                @teamSelected="selectTeam"
                hoverable
              />
            </div>
          </div>
        </div>
        <p class="subtitle">
          {{ userFullName }}
        </p>
      </header>
    </div>

    <div class="hero-foot">
      <dashboard-tabs
        :tabs="tabs"
        :currentTab="currentTab"
        @tabSelected="selectTab"
      />
    </div>
  </section>

  <keep-alive>
    <component v-bind:is="currentTabComponent" />
  </keep-alive>
</template>

<script>
import DashboardTabs from "./DashboardTabs.vue";
import TabServers from "./TabServers.vue";
import TabVolumes from "./TabVolumes.vue";
import TabSshKeys from "./TabSshKeys.vue";
import TabTeam from "./TabTeam.vue";
import TabUserProfile from "./TabUserProfile.vue";
import TabLicense from "./TabLicense.vue";
import TeamSelector from "./TeamSelector.vue";

export default {
  components: {
    DashboardTabs,
    TabServers,
    TabVolumes,
    TabSshKeys,
    TabTeam,
    TabUserProfile,
    TabLicense,
    TeamSelector,
  },
  data() {
    return {
      teams: null,
      teamsDataId: "teamsData",
      currentTeam: null,
      selectedTab: "servers",
      user: null,
      userDataId: "userData",
      tabs: {
        servers: "Servers",
        volumes: "Volumes",
        "ssh-keys": "SSH Keys",
        team: "Team Info",
        "user-profile": "User Profile",
        license: "License",
      },
      currentTab: "servers",
    };
  },
  computed: {
    userFullName() {
      return `${this.user.first_name} ${this.user.last_name}`;
    },
    currentTabComponent() {
      return "tab-" + this.currentTab;
    },
  },
  methods: {
    getTeams() {
      this.teams = JSON.parse(
        document.getElementById(this.teamsDataId).textContent
      );
      this.currentTeam = this.teams[0];
    },
    getUser() {
      this.user = JSON.parse(
        document.getElementById(this.userDataId).textContent
      );
      this.currentTeam = this.teams[0];
    },
    selectTeam(team) {
      this.currentTeam = team;
    },
    selectTab(key) {
      this.currentTab = key;
    },
  },
  beforeMount() {
    this.getTeams();
    this.getUser();
  },
};
</script>