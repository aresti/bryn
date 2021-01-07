<template>
  <template v-if="allInvitations.length">
    <div
      v-for="(invitation, index) in allInvitations"
      :key="index"
      class="panel-block"
    >
      <span class="panel-icon">
        <i class="fas fa-envelope" aria-hidden="true"></i>
      </span>
      <p class="is-flex-grow-1">
        {{ invitation.email }}
      </p>
      <base-button
        v-if="userIsAdmin"
        color="danger"
        size="small"
        rounded
        outlined
        @click="onDelete(invitation)"
        >Delete</base-button
      >
    </div>
  </template>
  <template v-else>
    <div class="panel-block"><p>No invitations pending</p></div>
  </template>

  <base-modal-delete
    v-if="confirmDeleteInvitation"
    verb="Delete"
    type="Invitation"
    :name="confirmDeleteInvitation.email"
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
      confirmDeleteInvitation: null,
      deleteProcessing: false,
    };
  },

  computed: {
    ...mapGetters(["userIsAdmin"]),
    ...mapGetters("invitations", ["allInvitations"]),
  },

  methods: {
    ...mapActions("invitations", ["deleteInvitation"]),
    onDelete(invitation) {
      this.confirmDeleteInvitation = invitation;
    },
    onCancelDelete() {
      this.confirmDeleteInvitation = null;
    },
    async onConfirmDelete() {
      if (this.deleteProcessing) {
        return;
      }
      const invitation = this.confirmDeleteInvitation;
      this.deleteProcessing = true;
      try {
        await this.deleteInvitation(invitation);
        this.toast(`Removed invitation: ${invitation.email}`);
      } catch (err) {
        this.toast.error(
          `Failed to remove invitation: ${
            err.response?.data.detail ?? "unexpected error"
          }`
        );
      } finally {
        this.confirmDeleteInvitation = null;
        this.deleteProcessing = false;
      }
    },
  },
};
</script>