<template>
  <span :class="containerClasses">
    <i :class="faClasses"></i>
  </span>
</template>

<script>
import bulmaColorMixin from "Mixins/bulmaColorMixin.js";
import bulmaSizeMixin from "Mixins/bulmaSizeMixin.js";

export default {
  mixins: [bulmaColorMixin, bulmaSizeMixin],
  props: {
    faClasses: {
      type: String,
      required: true,
    },
  },
  computed: {
    containerClasses() {
      return ["icon", this.sizeClass, this.textColorClass];
    },
  },
};
</script>