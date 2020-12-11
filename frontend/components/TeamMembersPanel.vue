<template>
  <nav class="panel">
    <p class="panel-heading">Team Members</p>
    <p class="panel-tabs">
      <a class="is-active">Members</a>
      <a>Invites</a>
    </p>
    <a
      v-for="(teamMember, index) in teamMembers"
      :key="index"
      class="panel-block is-active"
    >
      <span class="panel-icon">
        <i class="fas fa-user" aria-hidden="true"></i>
      </span>
      {{ teamMember.user.firstName }} {{ teamMember.user.lastName }}
    </a>
  </nav>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    teamMembers: {
      type: Array,
      required: true,
    },
  },
};
</script>