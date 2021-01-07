<template>
  <base-form-control
    :label="field.label ? field.label : titleCase(name)"
    :errors="field.errors"
    :expanded="field.element === 'select'"
    :required="!field.value && formFieldIsRequired(field)"
  >
    <template v-slot:default>
      <base-form-validated-input
        :name="name"
        :field="field"
        :disabled="disabled"
      />
    </template>
    <template v-if="field.iconClasses" v-slot:iconLeft>
      <base-icon :fa-classes="field.iconClasses" left :decorative="true" />
    </template>
    <template v-slot:iconRight>
      <base-icon
        :class="{
          'is-hidden': validationIconIsHidden,
        }"
        :fa-classes="validationIconClasses"
        :color="validationIconColor"
        right
        :decorative="true"
      />
    </template>
  </base-form-control>
</template>

<script>
import { titleCase } from "@/utils";
import formValidationMixin from "@/mixins/formValidationMixin";

export default {
  mixins: [formValidationMixin],

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

  setup() {
    return { titleCase };
  },

  computed: {
    validationIconIsHidden() {
      return (
        this.field.element === "select" ||
        !(this.field.value && this.field.hasOwnProperty("valid"))
      );
    },
    validationIconClasses() {
      return [
        "fas",
        { "fa-check": this.field.valid, "fa-times": !this.field.valid },
      ];
    },
    validationIconColor() {
      return this.field.valid ? "success" : "danger";
    },
  },
};
</script>