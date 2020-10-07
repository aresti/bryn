<template>
  <div class="alert" :class="contextClass" role="alert">
    <slot></slot>
  </div>
</template>

<script>
export default {
  props: {
    context: {
      type: String,
      default: "info",
    },
  },
  computed: {
    contextClass() {
      return `alert-${this.context}`;
    },
  },
};
</script>
