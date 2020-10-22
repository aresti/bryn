<template>
  <base-table fullwidth hoverable striped>
    <template v-slot:head>
      <tr>
        <th v-for="heading in headings" :key="heading">
          {{ heading }}
        </th>
      </tr>
    </template>
    <template v-slot:body>
      <instance-table-row-span v-if="loading">
        <base-progress
          color="primary"
          size="large"
          indeterminate
          class="mt-3"
        />
      </instance-table-row-span>
      <instance-table-row-span v-else-if="erroredOnGet">
        <base-message color="danger" dismissable>
          Your {{ tenant.region.description }} tenant seems to be unavailable
          right now.
        </base-message>
      </instance-table-row-span>
      <instance-table-row
        v-else
        v-for="instance in instances"
        :key="instance.uuid"
        :instance="instance"
      />
    </template>
  </base-table>
</template>

<script>
import BaseTable from "./BaseTable.vue";
import BaseMessage from "./BaseMessage.vue";
import BaseProgress from "./BaseProgress.vue";
import InstanceTableRow from "./InstanceTableRow.vue";
import InstanceTableRowSpan from "./InstanceTableRowSpan.vue";

export default {
  components: {
    BaseMessage,
    BaseProgress,
    BaseTable,
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
      headings: [
        "Name",
        "Flavor",
        "Status",
        "IP address",
        "Created",
        "Actions",
      ],
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