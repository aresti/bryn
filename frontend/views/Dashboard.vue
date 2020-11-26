<template>
  <div class="page-content">
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
  </div>

  <Footer class="mt-5" />
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import { useToast } from "vue-toastification";

import BaseDropdownList from "@/components/BaseDropdownList";
import BaseLevel from "@/components/BaseLevel";
import BaseLevelItem from "@/components/BaseLevelItem";
import BaseMessage from "@/components/BaseMessage";
import DashboardTabs from "@/components/DashboardTabs";
import Footer from "@/components/Footer";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },
  components: {
    BaseDropdownList,
    BaseLevel,
    BaseLevelItem,
    BaseMessage,
    DashboardTabs,
    Footer,
  },
  computed: {
    ...mapState(["user", "teams"]),
    ...mapGetters(["userFullName", "team", "tenants"]),
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
      console.log(this.tenants);
    }
  },
  mounted() {
    this.getAllTeamData();
  },
};
</script>

<style scoped>
.hero.is-primary {
  position: sticky;
  top: 56px;
  z-index: 999;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>