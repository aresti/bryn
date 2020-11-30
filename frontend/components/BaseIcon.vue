<template>
  <span :aria-hidden="decorative" :class="containerClasses">
    <i :class="faClasses"></i>
  </span>
</template>

<script>
import bulmaColorMixin from "@/mixins/bulmaColorMixin";
import bulmaSizeMixin from "@/mixins/bulmaSizeMixin";

export default {
  mixins: [bulmaColorMixin, bulmaSizeMixin],
  props: {
    decorative: {
      type: Boolean,
      default: false,
    },
    faClasses: {
      type: Array,
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