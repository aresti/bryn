<template>
  <instance-table v-if="tenant" :team="team" :tenant="tenant" />
</template>

<script>
import InstanceTable from "./InstanceTable.vue";

export default {
  components: {
    InstanceTable,
  },
  props: {
    team: {
      type: Object,
      required: true,
    },
    tenant: {
      type: Object,
      required: false,
    },
  },
};
</script>