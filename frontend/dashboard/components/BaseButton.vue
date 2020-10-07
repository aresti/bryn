<template>
  <button
    type="button"
    class="btn"
    :class="[isSmall ? smallClass : '', contextClass]"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  props: {
    context: {
      type: String,
      default: "info",
    },
    isOutline: {
      type: Boolean,
      default: false,
    },
    isSmall: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      smallClass: "btn-sm",
    };
  },
  computed: {
    contextClass() {
      return `btn-${this.isOutline ? "outline-" : ""}${this.context}`;
    },
  },
};
</script>
