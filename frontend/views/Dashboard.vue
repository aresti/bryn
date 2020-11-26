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
      </header>
    </div>

    <div class="hero-foot">
      <dashboard-tabs />
    </div>
  </section>

  <router-view v-slot="{ Component, route }">
    <transition name="fade" mode="out-in">
      <keep-alive>
        <component
          :is="Component"
          class="container mt-5"
          :class="'tab-' + route.name"
        />
      </keep-alive>
    </transition>
  </router-view>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import { useToast } from "vue-toastification";

import DashboardTabs from "@/components/DashboardTabs";
import BaseDropdownList from "@/components/BaseDropdownList";
import BaseMessage from "@/components/BaseMessage";
import Servers from "@/views/Servers";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },
  components: {
    DashboardTabs,
    BaseDropdownList,
    BaseMessage,
    Servers,
  },
  computed: {
    ...mapState(["user", "teams"]),
    ...mapGetters(["userFullName", "team"]),
  },
  methods: {
    ...mapActions(["setActiveTeam"]),
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
        this.toast.error(`Error fetching team instances: ${err.toString()}`);
      }
    },
    async getAllTeamData() {
      try {
        await this.$store.dispatch("flavors/getTeamFlavors");
      } catch (err) {
        this.toast.error(`Error fetching team data: ${err.toString()}`);
      }
      this.getTeamInstances();
    },
  },
  watch: {
    async team(_newTeam, _oldTeam) {
      this.getAllTeamData();
    },
  },
  beforeRouteUpdate(to, from) {
    // Update activeTeam on route change
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
  mounted() {
    this.getAllTeamData();
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
</style>