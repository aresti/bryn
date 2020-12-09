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
    <key-pairs-table :keypairs="keyPairsForFilterTenant" />

    <key-pairs-new-key-pair-modal
      v-if="showNewKeyPairModal"
      :key="activeTeam"
      @close-modal="showNewKeyPairModal = false"
    />
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import { mapGetters, mapState } from "vuex";

import BaseButton from "@/components/BaseButton";
import BaseButtonCreate from "@/components/BaseButtonCreate";
import BaseLevel from "@/components/BaseLevel";
import BaseLevelItem from "@/components/BaseLevelItem";
import KeyPairsNewKeyPairModal from "@/components/KeyPairsNewKeyPairModal";
import KeyPairsTable from "@/components/KeyPairsTable";
import TenantFilterTabs from "@/components/TenantFilterTabs";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

  components: {
    BaseButton,
    BaseButtonCreate,
    BaseLevel,
    BaseLevelItem,
    KeyPairsNewKeyPairModal,
    KeyPairsTable,
    TenantFilterTabs,
  },

  data() {
    return {
      showNewKeyPairModal: false,
    };
  },

  computed: {
    ...mapState(["activeTeam"]),
    ...mapGetters("keypairs", ["keyPairsForFilterTenant"]),
  },
};
</script>