<template>
  <span :class="containerClasses">
    <i :class="faClasses"></i>
  </span>
</template>

<script>
import bulmaColorMixin from "@/mixins/bulmaColorMixin";
import bulmaSizeMixin from "@/mixins/bulmaSizeMixin";

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