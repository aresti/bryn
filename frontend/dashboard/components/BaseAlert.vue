<template>
  <div class="alert" :class="contextClass" role="alert">
    <slot></slot>
    <button v-if="allowClose" @click="close" class="close" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
</template>

<script>
export default {
  emits: {
    "close-alert": null,
  },
  props: {
    context: {
      type: String,
      default: "info",
    },
    allowClose: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    contextClass() {
      return `alert-${this.context}`;
    },
  },
  methods: {
    close() {
      this.$emit("close-alert");
    },
  },
};
</script>
