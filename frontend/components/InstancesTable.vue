<template>
  <base-table fullwidth hoverable>
    <template v-slot:head>
      <tr>
        <th v-for="heading in headings" :key="heading">
          {{ heading }}
        </th>
      </tr>
    </template>
    <template v-slot:body>
      <instances-table-row
        v-for="instance in instances"
        :key="instance.uuid"
        :instance="instance"
      />
    </template>
  </base-table>
</template>

<script>
import InstancesTableRow from "@/components/InstancesTableRow";

export default {
  components: {
    InstancesTableRow,
  },
  props: {
    instances: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      headings: ["", "Server", "Flavor", "Status", "Created", ""],
    };
  },
};
</script>