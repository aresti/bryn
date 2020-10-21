<template>
  <progress :class="classList" :value="value" :max="max">{{ value }}%</progress>
</template>

<script>
import bulmaColorMixin from "Mixins/bulmaColorMixin.js";
import bulmaSizeMixin from "Mixins/bulmaSizeMixin.js";

export default {
  mixins: [bulmaColorMixin, bulmaSizeMixin],
  props: {
    value: {
      type: Number,
      default: 0,
    },
    max: {
      type: Number,
      default: 100,
    },
  },
  computed: {
    classList() {
      return ["progress", this.colorClass, this.sizeClass];
    },
  },
};
</script>