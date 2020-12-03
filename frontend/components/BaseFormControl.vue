<template>
  <div class="field">
    <label v-if="label.length" class="label">{{ label }}</label>
    <div class="control">
      <slot></slot>
    </div>
    <p v-if="error" class="help is-danger">
      {{ error }}
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
    error: {
      type: String,
      required: false,
    },
  },
};
</script>