<template>
  <div>
    <div class="block mb-3">
      <base-level>
        <template v-slot:left>
          <base-level-item>
            <h2 class="title">SSH Keys</h2>
          </base-level-item>
        </template>
        <template v-slot:right>
          <base-level-item>
            <base-button-create @click="showNewKeyPairModal = true">
              New SSH key pair
            </base-button-create>
          </base-level-item>
        </template>
      </base-level>
    </div>
    <key-pairs-table
      :keyPairs="keyPairs"
      @delete-keypair="onDeleteKeyPair"
      @set-default-keypair="onSetDefault"
    />

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
import { DELETE_KEY_PAIR, SET_DEFAULT_KEY_PAIR } from "@/store/action-types";

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

  computed: mapState({
    keyPairs: (state) => state.keyPairs.all,
  }),

  // Non-reactive
  methods: {
    ...mapActions({
      deleteKeyPair: DELETE_KEY_PAIR,
      setDefaultKeyPair: SET_DEFAULT_KEY_PAIR,
    }),

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
          `Failed to delete SSH key: ${err.response?.data.detail ?? err}`
        );
      } finally {
        this.confirmDeleteKeyPair = null;
        this.deleteProcessing = false;
      }
    },

    async onSetDefault(keyPair) {
      try {
        await this.setDefaultKeyPair(keyPair);
        this.toast(`Set default SSH key: ${keyPair.name}`);
      } catch (err) {
        this.toast.error(
          `Failed to set default SSH key: ${err.response?.data.detail ?? err}`
        );
      }
    },
  },
};
</script>