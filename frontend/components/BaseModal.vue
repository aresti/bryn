<template>
  <div class="modal is-active">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-content">
      <slot></slot>
    </div>
    <button
      class="modal-close is-large"
      aria-label="close"
      @click="closeModal"
    ></button>
  </div>
</template>

<script>
export default {
  emits: {
    "close-modal": null,
  },
  methods: {
    closeModal() {
      this.$emit("close-modal");
    },
  },
};
</script>