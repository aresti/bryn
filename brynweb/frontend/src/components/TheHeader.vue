<template>
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
          <template v-if="teams.length > 1" v-slot:right>
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
  </section>
</template>

<script>
import { mapGetters, mapState } from "vuex";

export default {
  computed: {
    ...mapState(["teams"]),
    ...mapGetters(["team", "userFullName"]),
  },
  methods: {
    onTeamSelect(team) {
      this.$router.push({
        name: this.$route.name,
        params: { teamId: team.id },
      });
    },
  },
};
</script>

<style scoped>
.hero {
  background: rgb(32, 60, 71);
  background: linear-gradient(
    0deg,
    rgba(32, 60, 71, 1) 0%,
    rgba(38, 70, 83, 1) 100%
  );
}
</style>