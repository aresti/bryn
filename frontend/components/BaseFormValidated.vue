<template>
  <form @submit.prevent="$emit('submit')" novalidate>
    <base-form-field v-for="[name, field] in Object.entries(form)" :key="name">
      <base-form-validated-control
        :field="field"
        :name="name"
        :disabled="disabled"
      />
    </base-form-field>

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
import formValidationMixin from "@/mixins/formValidationMixin";

export default {
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

  emits: ["submit"],

  computed: {
    submitDisabled() {
      if (this.requireInput) {
        return !(this.formIsValid && this.formIsDirty);
      } else {
        return !this.formIsValid;
      }
    },
  },
};
</script>