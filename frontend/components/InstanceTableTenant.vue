<template>
  <instance-table-row-span v-if="loading">
    <base-progress color="primary" size="large" value="null" class="mt-3" />
  </instance-table-row-span>
  <instance-table-row-span v-else-if="erroredOnGet">
    <base-message color="danger" dismissable>
      Your {{ tenant.region.description }} tenant seems to be unavailable right
      now.
    </base-message>
  </instance-table-row-span>
  <instance-table-row
    v-else
    v-for="instance in instances"
    :key="instance.uuid"
    :instance="instance"
  />
</template>

<script>
import BaseMessage from "./BaseMessage.vue";
import BaseProgress from "./BaseProgress.vue";
import InstanceTableRow from "./InstanceTableRow.vue";
import InstanceTableRowSpan from "./InstanceTableRowSpan.vue";

export default {
  components: {
    BaseMessage,
    BaseProgress,
    InstanceTableRow,
    InstanceTableRowSpan,
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