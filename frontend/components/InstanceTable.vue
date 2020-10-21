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
      <instance-table-tenant
        v-for="tenant in team.tenants"
        :key="tenant"
        :team="team"
        :tenant="tenant"
      />
    </template>
  </base-table>
</template>

<script>
import BaseTable from "./BaseTable.vue";
import InstanceTableTenant from "./InstanceTableTenant.vue";

export default {
  components: {
    BaseTable,
    InstanceTableTenant,
  },
  props: {
    team: {
      type: Object,
      required: true,
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