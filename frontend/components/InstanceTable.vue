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
import BaseTable from "@/components/BaseTable";
import BaseProgress from "@/components/BaseProgress";
import InstanceTableRow from "@/components/InstanceTableRow";
import InstanceTableRowSpan from "@/components/InstanceTableRowSpan";

export default {
  components: {
    BaseProgress,
    BaseTable,
    InstanceTableRow,
    InstanceTableRowSpan,
  },
  props: {
    instances: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      headings: [
        "Region",
        "Name",
        "Flavor",
        "Status",
        "IP address",
        "Created",
        "Actions",
      ],
    };
  },
};
</script>