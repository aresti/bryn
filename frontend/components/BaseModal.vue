<template>
  <!-- Modal -->
  <div @click="closeModal" class="modal-background">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">
            <slot name="header"></slot>
          </h5>
          <button
            @click="closeModal"
            type="button"
            class="close"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.modal-background {
  background-color: rgba(10, 10, 10, 0.86);
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  top: 0;
  z-index: 40;
}
</style>

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
