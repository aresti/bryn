<template>
  <tr>
    <td v-for="value in rowValues" :key="value">
      {{ value }}
    </td>
    <td>Menu</td>
  </tr>
</template>

<script>
export default {
  props: {
    instance: {
      type: Object,
      required: true,
    },
  },
  computed: {
    rowValues() {
      return [
        this.instance.name,
        this.instance.flavor,
        this.instance.status,
        this.instance.ip,
        this.instance.created,
      ];
    },
  },
};
</script>