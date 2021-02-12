<template>
  <base-hero-full v-if="teams.length" centered>
    <h2 class="subtitle">Initializing team admin console...</h2>
    <base-progress indeterminate color="success" />
  </base-hero-full>
  <no-teams v-else />
</template>

<script>
import { mapState } from "vuex";
import NoTeams from "@/components/NoTeams";

export default {
  components: {
    NoTeams,
  },
  computed: mapState(["teams"]),
  mounted() {
    if (this.teams.length) {
      const defaultTeam = this.teams[0];
      this.$router.push({
        name: "teamHome",
        params: { teamId: defaultTeam.id },
      });
    }
  },
};
</script>