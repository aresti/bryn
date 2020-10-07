<template>
  <section v-if="errored">
    <base-alert context="danger">
      Sorry, team data doesn't seem to be available right now.
      <hr />
      Please try back later.
    </base-alert>
  </section>

  <section v-else>
    <base-alert v-if="loading" context="light">Loading...</base-alert>
    <team-member-list :team-members="teamMembers"></team-member-list>
  </section>
</template>

<script>
import axios from "axios";
import TeamMemberList from "./TeamMemberList.vue";
import BaseAlert from "./BaseAlert.vue";

export default {
  components: {
    TeamMemberList,
    BaseAlert,
  },
  props: {
    teamId: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      teamMembers: [],
      loading: true,
      errored: false,
    };
  },
  mounted() {
    axios
      .get(`/user/api/teams/${this.teamId}/members/?format=json`)
      .then((response) => (this.teamMembers = response.data))
      .catch((error) => {
        console.log(error);
        this.errored = true;
      })
      .finally(() => (this.loading = false));
  },
};
</script>
