<template>
  <team-member-list :team-id="teamId"></team-member-list>
</template>

<script>
import TeamMemberList from "./TeamMemberList.vue";

export default {
  components: {
    TeamMemberList,
  },
  props: {
    teamId: {
      required: true,
      type: Number,
    },
  },
};
</script>
