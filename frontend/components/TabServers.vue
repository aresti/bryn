<template>
  <instance-table :team="team" />
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
  },
};
</script>