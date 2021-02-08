<template>
  <div>
    <div class="columns">
      <div class="column is-12">
        <base-level>
          <template v-slot:left>
            <h2 class="title">Team Profile</h2>
          </template>
          <template v-slot:right>
            <base-level-item>
              <base-button-create @click="showNewInvitationModal = true">
                New Invitation
              </base-button-create>
            </base-level-item>
          </template>
        </base-level>
      </div>
    </div>
    <div class="columns">
      <div class="column content">
        <team-profile />
      </div>
      <div class="column">
        <team-members-panel :teamMembers="allTeamMembers" />
        <base-notification color="success">
          Your team licence is valid until 28/01/2021
        </base-notification>
      </div>
    </div>

    <team-new-invitation-modal
      v-if="showNewInvitationModal"
      @closeModal="showNewInvitationModal = false"
    />
  </div>
</template>

<script>
import TeamMembersPanel from "@/components/TeamMembersPanel";
import TeamNewInvitationModal from "@/components/TeamNewInvitationModal";
import TeamProfile from "@/components/TeamProfile";

import { mapGetters } from "vuex";

export default {
  components: {
    TeamMembersPanel,
    TeamNewInvitationModal,
    TeamProfile,
  },

  data() {
    return {
      showNewInvitationModal: false,
    };
  },

  computed: {
    ...mapGetters(["team"]),
    ...mapGetters("teamMembers", ["allTeamMembers"]),
  },
};
</script>

