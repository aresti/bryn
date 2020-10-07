<template>
  <template v-if="erroredOnGet">
    <base-alert context="danger">
      Sorry, team data doesn't seem to be available right now.
      <hr />
      Please try back later.
    </base-alert>
  </template>

  <template v-else>
    <base-alert v-if="loading" context="light">Loading...</base-alert>
    <ul class="list-group">
      <team-member-list-item
        v-for="member in teamMembers"
        v-bind:member="member"
        v-bind:key="member.id"
        @delete-member="deleteMember(member)"
      ></team-member-list-item>
    </ul>
  </template>

  <template v-if="erroredOnDelete">
    <base-alert
      context="danger"
      class="mt-2"
      allow-close
      @close-alert="erroredOnDelete = false"
    >
      Sorry, an error occurred when trying to remove this team member.
    </base-alert>
  </template>
</template>

<script>
import TeamMemberListItem from "./TeamMemberListItem.vue";
import BaseAlert from "./BaseAlert.vue";

export default {
  inject: ["axios"],
  components: {
    TeamMemberListItem,
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
      erroredOnGet: false,
      erroredOnDelete: false,
    };
  },
  methods: {
    getMembers() {
      this.axios
        .get(`/user/api/teams/${this.teamId}/members/?format=json`)
        .then((response) => (this.teamMembers = response.data))
        .catch((error) => {
          console.log(error.toJSON());
          this.erroredOnGet = true;
        })
        .finally(() => (this.loading = false));
    },
    deleteMember: async function (member) {
      this.erroredOnDelete = false;
      try {
        await this.axios.delete(
          `/user/api/teams/${this.teamId}/members/${member.id}`
        );
        this.getMembers();
      } catch (error) {
        if (error.response) {
          console.log(error.response.data);
        }
        this.erroredOnDelete = true;
      }
    },
  },
  mounted() {
    this.getMembers();
  },
};
</script>
