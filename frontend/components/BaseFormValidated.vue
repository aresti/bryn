<template>
  <form @submit.prevent="$emit('submit')" novalidate>
    <base-form-control
      v-for="[key, value] in Object.entries(form)"
      :key="key"
      :label="value.label ? value.label : titleCase(key)"
      :errors="value.errors"
      :expanded="value.element === 'select'"
    >
      <base-form-field-select
        v-if="value.element === 'select'"
        v-model="value.value"
        :name="key"
        :options="value.options"
        :null-option-label="`Select a ${value.label ?? key}`"
        :invalid="formFieldIsInvalid(value)"
        :disabled="disabled"
        @validate="formValidateField(key)"
        @change="formDirtyField(key)"
        fullwidth
      />
      <base-form-field
        v-else
        v-model.trim="value.value"
        :name="key"
        :element="value.element"
        :invalid="formFieldIsInvalid(value)"
        :disabled="disabled"
        @validate="formValidateField(key)"
        @input="formDirtyField(key)"
      />
    </base-form-control>

    <ul v-if="nonFieldErrors?.length" class="has-text-danger">
      <template v-for="err in nonFieldErrors" :key="err">
        <li>{{ err.message }}</li>
      </template>
    </ul>

    <slot name="buttons"
      ><base-button-confirm
        type="submit"
        :disabled="submitDisabled || disabled"
        :loading="submitted"
        >{{ submitLabel }}</base-button-confirm
      ></slot
    >
  </form>
</template>

<script>
import { titleCase } from "@/utils";
import formValidationMixin from "@/mixins/formValidationMixin";

export default {
  setup() {
    return { titleCase };
  },

  mixins: [formValidationMixin],

  props: {
    form: {
      type: Object,
      required: true,
    },
    nonFieldErrors: {
      type: Array,
      required: false,
    },
    requireInput: {
      type: Boolean,
      default: false,
    },
    submitLabel: {
      type: String,
      default: "Submit",
    },
    submitted: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },

  emits: ["validate-field", "submit"],

  computed: {
    submitDisabled() {
      if (this.requireInput) {
        return !(this.formIsValid && this.formIsDirty);
      } else {
        return !this.formIsValid;
      }
    },
  },

  methods: {
    emitValidate(name) {
      this.$emit("validate-field", name);
    },
  },
};
</script>