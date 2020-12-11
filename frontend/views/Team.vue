<template>
  <div class="columns">
    <div class="column content">
      <team-profile />
    </div>
    <div class="column">
      <team-members-panel :teamMembers="teamMembers" />
      <base-notification color="success">
        Your team licence is valid until 28/01/2021
      </base-notification>
    </div>
  </div>
</template>

<script>
import TeamMembersPanel from "@/components/TeamMembersPanel";
import TeamProfile from "@/components/TeamProfile";

import { mapState, mapGetters } from "vuex";

export default {
  components: {
    TeamMembersPanel,
    TeamProfile,
  },
  computed: {
    ...mapState({
      teamMembers: (state) => state.teamMembers.all,
    }),
    ...mapGetters(["team"]),
  },
};
</script>

