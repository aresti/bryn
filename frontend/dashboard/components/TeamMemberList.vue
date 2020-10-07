<template>
  <ul class="list-group">
    <team-member-list-item
      v-for="member in teamMembers"
      v-bind:member="member"
      v-bind:key="member.id"
    ></team-member-list-item>
  </ul>
</template>

<script>
import TeamMemberListItem from "./TeamMemberListItem.vue";

export default {
  components: {
    TeamMemberListItem,
  },
  props: {
    teamMembers: {
      required: true,
      type: Array,
    },
  },
};
</script>
