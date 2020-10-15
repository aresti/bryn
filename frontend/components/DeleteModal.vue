<template>
  <base-modal>
    <template v-slot:header>{{ verb }} {{ entityName }}?</template>

    <template v-slot:default>
      <p>Are you sure you wish to {{ verb }} {{ deleteName }}?</p>
    </template>

    <template v-slot:footer>
      <cancel-button>Cancel</cancel-button>
      <delete-button>{{ verb }}</delete-button>
    </template>
  </base-modal>
</template>

<script>
export default {
  emits: {
    "confirm-delete": null,
    "close-modal": null
  },
  props: {
    verb: {
      required: false,
      type: String,
      default: "remove"
    },
    erroredOnDelete: {
      required: false,
      type: Boolean,
      default: false
    },
  },
  methods: {
    confirmDelete() {
      this.$emit("confirm-delete");
    },
    closeModal() {
      this.$emit("close-modal");
    },
  },
};
</script>