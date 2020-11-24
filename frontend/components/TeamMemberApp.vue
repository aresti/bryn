<template>
  <section class="mb-4">
    <h5>Team members</h5>
    <team-member-list :team-id="teamId" />
  </section>

  <section class="mb-4">
    <h5>Pending invites</h5>
    <team-invite-list :team-id="teamId" />
  </section>
</template>

<script>
import TeamMemberList from "@/components/TeamMemberList";
import TeamInviteList from "@/components/TeamInviteList";

export default {
  components: {
    TeamMemberList,
    TeamInviteList,
  },
  props: {
    teamId: {
      required: true,
      type: Number,
    },
  },
};
</script>
