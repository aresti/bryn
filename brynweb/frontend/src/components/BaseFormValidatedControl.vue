<template>
  <base-form-control
    :label="field.label"
    :errors="field.errors"
    :expanded="field.element === 'select'"
    :required="!field.value && field.required"
  >
    <template v-slot:default>
      <base-form-validated-input
        :name="name"
        :field="field"
        :disabled="disabled"
      />
    </template>
    <template v-if="field.iconClasses" v-slot:iconLeft>
      <base-icon :icon="field.iconClasses" left :decorative="true" />
    </template>
    <template v-slot:iconRight>
      <base-icon
        :class="{
          'is-hidden': !field.error,
        }"
        :icon="['fas', 'times']"
        color="danger"
        right
        :decorative="true"
      />
    </template>
  </base-form-control>
</template>

<script>
export default {
  props: {
    field: {
      type: Object,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
};
</script>