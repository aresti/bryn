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
      <p class="is-flex-grow-1">
        {{ teamMember.user.firstName }} {{ teamMember.user.lastName }}
      </p>
      <base-tag v-if="teamMember.isAdmin" class="ml-3" color="dark" rounded
        >Admin</base-tag
      >
      <base-button
        v-if="!teamMember.isAdmin && userIsAdmin"
        color="danger"
        size="small"
        rounded
        outlined
        @click="onDelete(teamMember)"
        >Remove</base-button
      >
    </a>
  </nav>

  <base-modal-delete
    v-if="confirmDeleteTeamMember"
    verb="Remove"
    type="Team
  Member"
    :name="fullName(confirmDeleteTeamMember)"
    :processing="deleteProcessing"
    @close-modal="onCancelDelete"
    @confirm-delete="onConfirmDelete"
  />
</template>

<script>
import { useToast } from "vue-toastification";
import { mapActions, mapGetters } from "vuex";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

  data() {
    return {
      confirmDeleteTeamMember: null,
      deleteProcessing: false,
    };
  },

  props: {
    teamMembers: {
      type: Array,
      required: true,
    },
  },

  computed: {
    ...mapGetters(["userIsAdmin"]),
  },

  methods: {
    ...mapActions("teamMembers", ["deleteTeamMember"]),
    fullName(teamMember) {
      return `${teamMember.user.firstName} ${teamMember.user.lastName}`;
    },
    onDelete(teamMember) {
      this.confirmDeleteTeamMember = teamMember;
    },
    onCancelDelete() {
      this.confirmDeleteTeamMember = null;
    },
    async onConfirmDelete() {
      if (this.deleteProcessing) {
        return;
      }
      const teamMember = this.confirmDeleteTeamMember;
      this.deleteProcessing = true;
      try {
        await this.deleteTeamMember(teamMember);
        this.toast(`Removed team member: ${this.fullName(teamMember)}`);
      } catch (err) {
        this.toast.error(
          `Failed to remove team member: ${
            err.response?.data.detail ?? "unexpected error"
          }`
        );
      } finally {
        this.confirmDeleteTeamMember = null;
        this.deleteProcessing = false;
      }
    },
  },
};
</script>