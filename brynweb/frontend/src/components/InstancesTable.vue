<template>
  <base-table fullwidth hoverable>
    <template v-slot:head>
      <tr>
        <th>Name</th>
        <th>Flavor</th>
        <th>Status</th>
        <th class="is-hidden-touch">Created</th>
        <th><!-- Action buttons --></th>
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
};
</script>