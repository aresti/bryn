<template>
  <main>
    <template v-if="erroredOnGet">
      <base-message color="danger" dismissable>
        An error occurred while trying to get your servers. Your tenant(s) may
        be temporarily unavailable.
      </base-message>
    </template>
    <template v-else>
      <div class="container mb-3">
        <base-button-create @click="showLaunchInstanceModal = true"
          >New server</base-button-create
        >
      </div>
      <instance-table :instances="instances" :loading="loading" />
    </template>

    <launch-instance-modal
      v-if="showLaunchInstanceModal"
      @close-modal="showLaunchInstanceModal = false"
    />
  </main>
</template>

<script>
import { useToast } from "vue-toastification";
import { mapGetters, mapState } from "vuex";

import BaseButtonCreate from "@/components/BaseButtonCreate";
import BaseMessage from "@/components/BaseMessage";
import LaunchInstanceModal from "@/components/LaunchInstanceModal";
import InstanceTable from "@/components/InstanceTable";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },
  components: {
    BaseButtonCreate,
    BaseMessage,
    LaunchInstanceModal,
    InstanceTable,
  },
  data() {
    return {
      showLaunchInstanceModal: false,
    };
  },
  computed: {
    ...mapState("instances", {
      loading: (state) => state.loading,
      erroredOnGet: (state) => state.erroredOnGet,
    }),
    ...mapGetters("instances", {
      instances: "allFormatted",
    }),
  },
};
</script>