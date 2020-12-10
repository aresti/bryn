<template>
  <div class="field">
    <label v-if="label.length" class="label">{{ label }}</label>
    <div :class="controlClasses">
      <slot></slot>
    </div>
    <p v-if="errors?.length" class="help is-danger">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      required: false,
    },
    errors: {
      type: Array,
      required: false,
    },
    expanded: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    errorMessage() {
      /* Derives a single error message from an expected array of ValidationError objects */
      return this.errors?.map((err) => err.message).join(", ");
    },
    controlClasses() {
      return ["control", { "is-expanded": this.expanded }];
    },
  },
};
</script>