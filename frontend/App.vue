<template>
  <template v-if="initialized">
    <router-view v-if="teams.length" />
    <no-teams v-else />
  </template>
  <template v-else>
    <initializing />
  </template>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Initializing from "@/components/Initializing";
import NoTeams from "@/components/NoTeams";

export default {
  components: {
    Initializing,
    NoTeams,
  },
  computed: mapState(["initialized", "teams"]),
  methods: mapActions(["setActiveTeam"]),
  watch: {
    initialized() {
      // Navigate to default team dashboard
      if (this.teams.length) {
        const team = this.teams[0];
        this.setActiveTeam(team);
        this.$router.push({
          name: "dashboard",
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