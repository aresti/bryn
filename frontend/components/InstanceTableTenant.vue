<template>
  <instance-table-row-loading
    v-if="loading"
    size="large"
    color="success"
    value="null"
  />
  <instance-table-row
    v-else
    v-for="instance in instances"
    :key="instance.uuid"
    :instance="instance"
  />
</template>

<script>
import BaseProgress from "./BaseProgress.vue";
import InstanceTableRow from "./InstanceTableRow.vue";
import InstanceTableRowLoading from "./InstanceTableRowLoading.vue";

export default {
  components: {
    BaseProgress,
    InstanceTableRow,
    InstanceTableRowLoading,
  },
  props: {
    team: {
      type: Object,
      required: true,
    },
    tenant: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      instances: [],
      loading: true,
      erroredOnGet: false,
    };
  },
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