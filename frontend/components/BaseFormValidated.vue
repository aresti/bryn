<template>
  <form @submit.prevent="$emit('submit')" novalidate>
    <base-form-control
      v-for="[key, value] in Object.entries(fields)"
      :key="key"
      :label="value.label ? value.label : key"
      :errors="value.errors"
      :expanded="value.element === 'select'"
    >
      <base-form-field-select
        v-if="value.element === 'select'"
        v-model="value.value"
        :name="key"
        :options="value.options"
        :null-option-label="`Select a ${key}`"
        :invalid="fieldIsInvalid(value)"
        @validate="emitValidate(key)"
        fullwidth
      />
      <base-form-field
        v-else
        v-model="value.value"
        :name="key"
        :element="value.element"
        :invalid="fieldIsInvalid(value)"
        @validate="emitValidate(key)"
      />
    </base-form-control>

    <slot name="buttons"
      ><base-button-confirm type="submit" :disabled="!formValid">{{
        submitLabel
      }}</base-button-confirm></slot
    >
  </form>
</template>

<script>
export default {
  props: {
    fields: {
      type: Object,
      required: true,
    },
    submitLabel: {
      type: String,
      default: "Submit",
    },
  },
  emits: ["validate-field", "submit"],
  computed: {
    formValid() {
      return Object.values(this.fields).every(
        (fieldObj) => fieldObj.valid || !fieldObj.validators?.length
      );
    },
  },
  methods: {
    fieldIsInvalid(field) {
      return Boolean(field.errors?.length);
    },
    emitValidate(name) {
      this.$emit("validate-field", name);
    },
  },
};
</script>