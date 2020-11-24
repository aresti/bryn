<template>
  <main>
    <template v-if="erroredOnGet">
      <base-message color="danger" dismissable>
        Your {{ tenant.region_name }} tenant seems to be unavailable right now.
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
import { mapGetters } from "vuex";

import BaseButtonCreate from "@/components/BaseButtonCreate";
import BaseMessage from "@/components/BaseMessage";
import LaunchInstanceModal from "@/components/LaunchInstanceModal";
import InstanceTable from "@/components/InstanceTable";

export default {
  components: {
    BaseButtonCreate,
    BaseMessage,
    LaunchInstanceModal,
    InstanceTable,
  },
  data() {
    return {
      instances: [],
      loading: true,
      erroredOnGet: false,
      showLaunchInstanceModal: false,
    };
  },
  computed: mapGetters(["team", "tenant"]),
  methods: {
    async getInstances() {
      try {
        const response = await this.$http.get(
          `/api/teams/${this.team.id}/tenants/${this.tenant.id}/instances/?format=json`
        );
        this.instances = response.data;
      } catch (error) {
        this.erroredOnGet = true;
      }
      this.loading = false;
    },
  },
  mounted() {
    this.getInstances();
  },
};
</script>