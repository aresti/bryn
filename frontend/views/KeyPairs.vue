<template>
  <div>
    <div class="block mb-3">
      <base-level>
        <template v-slot:right>
          <base-level-item>
            <base-button-create @click="showNewKeyPairModal = true">
              New SSH key pair
            </base-button-create>
          </base-level-item>
        </template>
      </base-level>
    </div>
    <key-pairs-table :keyPairs="keyPairs" @delete-keypair="onDeleteKeyPair" />

    <div v-if="!keyPairs.length" class="content has-text-centered">
      <h4 class="subtitle">You haven't created any SSH keys yet</h4>
    </div>

    <key-pairs-new-key-pair-modal
      v-if="showNewKeyPairModal"
      @close-modal="showNewKeyPairModal = false"
    />

    <base-modal-delete
      v-if="confirmDeleteKeyPair"
      verb="Delete"
      type="SSH key"
      :name="confirmDeleteKeyPair.name"
      :processing="deleteProcessing"
      @close-modal="onCancelDelete"
      @confirm-delete="onConfirmDelete"
    />
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

import KeyPairsNewKeyPairModal from "@/components/KeyPairsNewKeyPairModal";
import KeyPairsTable from "@/components/KeyPairsTable";

export default {
  // Template dependencies
  components: {
    KeyPairsNewKeyPairModal,
    KeyPairsTable,
  },

  // Composition
  inject: ["toast"],

  // Local state
  data() {
    return {
      showNewKeyPairModal: false,
      confirmDeleteKeyPair: null,
      deleteProcessing: false,
    };
  },

  computed: mapState("keyPairs", {
    keyPairs: (state) => state.all,
  }),

  // Non-reactive
  methods: {
    ...mapActions("keyPairs", ["deleteKeyPair"]),
    onDeleteKeyPair(keyPair) {
      this.confirmDeleteKeyPair = keyPair;
    },
    onCancelDelete() {
      this.confirmDeleteKeyPair = null;
    },
    async onConfirmDelete() {
      if (this.deleteProcessing) {
        return;
      }
      const keyPair = this.confirmDeleteKeyPair;
      this.deleteProcessing = true;
      try {
        await this.deleteKeyPair(keyPair);
        this.toast(`Deleted SSH key: ${keyPair.name}`);
      } catch (err) {
        this.toast.error(
          `Failed to delete SSH key: ${
            err.response?.data.detail ?? "unexpected error"
          }`
        );
      } finally {
        this.confirmDeleteKeyPair = null;
        this.deleteProcessing = false;
      }
    },
  },
};
</script>