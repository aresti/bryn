<template>
  <template v-if="initialized">
    <router-view v-if="teams.length"></router-view>
    <no-teams v-else />
  </template>
  <template v-else>
    <initializing />
  </template>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Initializing from "@/components/Initializing.vue";
import NoTeams from "@/components/NoTeams.vue";

export default {
  components: {
    Initializing,
    NoTeams,
  },
  computed: {
    ...mapState(["initialized", "teams"]),
  },
  methods: {
    ...mapActions(["setActiveTeam"]),
  },
  watch: {
    initialized() {
      // Navigate to default team dashboard
      if (this.teams.length) {
        const team = this.teams[0];
        this.setActiveTeam(team);
        this.$router.push({
          name: "Dashboard",
          params: { teamId: team.id },
        });
      }
    },
  },
  beforeMount() {
    this.$store.dispatch("initStore");
  },
};
</script>