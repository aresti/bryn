<template>
  <base-table hoverable>
    <template v-slot:head>
      <th>Team members</th>
    </template>
    <template v-slot:body>
      <tr v-for="(teamMember, index) in teamMembers" :key="index">
        <td>{{ teamMember.user.firstName }} {{ teamMember.user.lastName }}</td>
      </tr>
    </template>
  </base-table>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    teamMembers: {
      type: Array,
      required: true,
    },
  },
};
</script>