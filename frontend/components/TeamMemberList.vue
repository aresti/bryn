<template>
  <fetch-error-alert v-if="erroredOnGet" />

  <template v-else>
    <base-alert v-if="loading" context="light">Loading...</base-alert>

    <ul class="list-group">
      <team-member-list-item
        v-for="member in teamMembers"
        v-bind:member="member"
        v-bind:key="member.id"
        @delete-member="confirmDeleteMember(member)"
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

  <base-modal v-if="showDeleteModal" @close-modal="showDeleteModal = false">
    <template v-slot:header>Remove {{ deleteName }}?</template>

    <template v-slot:default>
      <p>Are you sure you wish to remove {{ deleteName }} from the team?</p>
    </template>

    <template v-slot:footer>
      <cancel-button @click="showDeleteModal = false">Cancel</cancel-button>
      <delete-button @click="deleteMember">Remove</delete-button>
    </template>
  </base-modal>
</template>

<script>
import TeamMemberListItem from "./TeamMemberListItem.vue";
import BaseAlert from "./BaseAlert.vue";
import BaseModal from "./BaseModal.vue";
import CancelButton from "./CancelButton.vue";
import DeleteButton from "./DeleteButton.vue";
import FetchErrorAlert from "./FetchErrorAlert.vue";

export default {
  components: {
    TeamMemberListItem,
    BaseAlert,
    BaseModal,
    CancelButton,
    DeleteButton,
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
      teamMembers: [],
      loading: true,
      erroredOnGet: false,
      erroredOnDelete: false,
      memberToDelete: null,
      showDeleteModal: false,
    };
  },
  computed: {
    deleteName() {
      const user = this.memberToDelete.user;
      return [user.first_name, user.last_name].join(" ");
    },
  },
  methods: {
    getMembers() {
      this.$http
        .get(`/user/api/teams/${this.teamId}/members/?format=json`)
        .then((response) => (this.teamMembers = response.data))
        .catch((error) => {
          this.erroredOnGet = true;
        })
        .finally(() => (this.loading = false));
    },
    confirmDeleteMember(member) {
      this.memberToDelete = member;
      this.showDeleteModal = true;
    },
    deleteMember: async function () {
      if (!this.memberToDelete) {
        return;
      }
      this.erroredOnDelete = false;

      try {
        await this.$http.delete(
          `/user/api/teams/${this.teamId}/members/${this.memberToDelete.id}`
        );
        this.memberToDelete = null;
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
