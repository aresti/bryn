<template>
  <base-form-input-select
    v-if="field.element === 'select'"
    v-model="field.value"
    :name="name"
    :options="field.options"
    :null-option-label="`Select a ${field.label ?? name}`"
    :invalid="formFieldIsInvalid(field)"
    @validate="formValidateField(field)"
    @change="formDirtyField(field)"
    fullwidth
  />
  <base-form-input
    v-else
    v-model.trim="field.value"
    :name="name"
    :element="field.element"
    :invalid="formFieldIsInvalid(field)"
    @validate="debouncedValidator"
    @input="formDirtyField(field)"
  />
</template>

<script>
import { debounce } from "@/utils";
import formValidationMixin from "@/mixins/formValidationMixin";

export default {
  mixins: [formValidationMixin],

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

  computed: {
    debouncedValidator() {
      return debounce(this.formCreateFieldValidator(this.field));
    },
  },
};
</script>