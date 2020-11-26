<template>
  <base-hero-full v-if="teams.length" centered>
    <h2 class="subtitle">Initializing team dashboard...</h2>
    <base-progress indeterminate color="success" />
  </base-hero-full>
  <no-teams v-else />
</template>

<script>
import { mapState } from "vuex";
import NoTeams from "@/components/NoTeams";
import BaseHeroFull from "@/components/BaseHeroFull";
import BaseProgress from "@/components/BaseProgress";

export default {
  components: {
    BaseHeroFull,
    BaseProgress,
    NoTeams,
  },
  computed: mapState(["teams"]),
  mounted() {
    if (this.teams.length) {
      const defaultTeam = this.teams[0];
      this.$router.push({
        name: "dashboard",
        params: { teamId: defaultTeam.id },
      });
    }
  },
};
</script>