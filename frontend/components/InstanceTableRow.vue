<template>
  <tr>
    <td
      v-for="(value, index) in rowValues"
      :key="value"
      :class="{ 'has-text-success': value === 'ACTIVE' }"
    >
      <base-icon
        v-if="index === 0"
        :fa-classes="['fa', 'fa-server']"
        class="mr-2"
      />
      {{ value }}
    </td>
    <td>Menu</td>
  </tr>
</template>

<script>
import BaseIcon from "./BaseIcon";
export default {
  components: { BaseIcon },
  props: {
    instance: {
      type: Object,
      required: true,
    },
  },
  computed: {
    rowValues() {
      return [
        this.instance.region,
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