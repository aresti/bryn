<template>
  <progress v-if="indeterminate" :class="classList"></progress>
  <progress v-else :value="valueAttr" :max="max">{{ value }}%</progress>
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
    indeterminate: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    classList() {
      return ["progress", this.colorClass, this.sizeClass];
    },
  },
};
</script>