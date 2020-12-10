<template>
  <fetch-error-alert v-if="erroredOnGet" />

  <template v-else>
    <base-alert v-if="loading" context="light">Loading...</base-alert>

    <ul class="list-group">
      <team-invite-list-item
        v-for="invite in teamInvites"
        v-bind:invite="invite"
        v-bind:key="invite.email"
      ></team-invite-list-item>
    </ul>
  </template>
</template>

<script>
import TeamInviteListItem from "@/components/TeamInviteListItem";
import FetchErrorAlert from "@/components/FetchErrorAlert";

export default {
  inject: ["axios"],
  components: {
    TeamInviteListItem,
    FetchErrorAlert,
  },
  props: {
    teamId: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      teamInvites: [],
      loading: true,
      erroredOnGet: false,
    };
  },
  methods: {
    getInvites() {
      this.axios
        .get(`/user/api/teams/${this.teamId}/invitations/?format=json`)
        .then((response) => (this.teamInvites = response.data))
        .catch((error) => {
          this.erroredOnGet = true;
        })
        .finally(() => (this.loading = false));
    },
  },
  mounted() {
    this.getInvites();
  },
};
</script>
