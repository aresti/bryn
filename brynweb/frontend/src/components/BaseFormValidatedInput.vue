<template>
  <base-form-input-select
    v-if="field.element === 'select'"
    v-model="field.value"
    v-bind="selectedAttrs"
    @change="field.touch()"
  />
  <base-form-input
    v-else
    v-model.trim="field.value"
    v-bind="field.element === 'textarea' ? sharedAttrs : inputAttrs"
    :element="field.element"
    @input="debouncedTouch(500)"
    @blur="debouncedTouch(0)"
  />
</template>

<script>
export default {
  props: {
    name: {
      type: String,
      required: true,
    },
    field: {
      type: Object,
      required: false,
    },
  },

  setup(props) {
    // Debounced touch func
    let timeout;
    const debouncedTouch = (wait = 500) => {
      clearTimeout(timeout);
      timeout = setTimeout(props.field.touch, wait);
    };
    return { debouncedTouch };
  },

  computed: {
    sharedAttrs() {
      // Applicable to all elements (input, textarea & select)
      return {
        name: this.field.name,
        invalid: this.field.invalid,
      };
    },
    inputAttrs() {
      // Input attributes
      return {
        ...this.sharedAttrs,
        type: this.field.type,
      };
    },
    selectedAttrs() {
      // Select attributes
      return {
        ...this.sharedAttrs,
        options: this.field.options,
        "null-option-label": `Select a ${this.field.label}`,
        fullwidth: true,
      };
    },
  },
};
</script>