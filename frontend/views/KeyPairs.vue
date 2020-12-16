<template>
  <div>
    <div class="block mb-3">
      <base-level>
        <template v-slot:left>
          <base-level-item>
            <tenant-filter-tabs />
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
      :keyPairs="keyPairsForFilterTenant"
      @delete-keypair="onDeleteKeyPair"
    />

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
import { useToast } from "vue-toastification";
import { mapActions, mapGetters, mapState } from "vuex";

import KeyPairsNewKeyPairModal from "@/components/KeyPairsNewKeyPairModal";
import KeyPairsTable from "@/components/KeyPairsTable";
import TenantFilterTabs from "@/components/TenantFilterTabs";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

  components: {
    KeyPairsNewKeyPairModal,
    KeyPairsTable,
    TenantFilterTabs,
  },

  data() {
    return {
      showNewKeyPairModal: false,
      confirmDeleteKeyPair: null,
      deleteProcessing: false,
    };
  },

  computed: {
    ...mapState(["activeTeam"]),
    ...mapGetters("keyPairs", ["keyPairsForFilterTenant"]),
  },

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
        this.toast.warning(`Deleted SSH key: ${keyPair.name}`);
      } catch (err) {
        this.toast.error(`Failed to delete SSH key: ${err.message}`);
      } finally {
        this.confirmDeleteKeyPair = null;
        this.deleteProcessing = false;
      }
    },
  },
};
</script>