<template>
  <component
    :is="element"
    :name="name"
    :value="modelValue"
    @input="onInput"
    @blur="emitValidate"
    @change="emitValidate"
    :class="classes"
    :spellcheck="spellcheck"
  />
</template>

<script>
import bulmaColorMixin from "@/mixins/bulmaColorMixin";
import bulmaSizeMixin from "@/mixins/bulmaSizeMixin";

export default {
  mixins: [bulmaColorMixin, bulmaSizeMixin],
  props: {
    modelValue: {
      type: undefined,
      required: false,
    },
    element: {
      type: String,
      default: "input",
    },
    name: {
      type: String,
      required: true,
    },
    invalid: {
      type: Boolean,
      default: false,
    },
    fullwidth: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    rounded: {
      type: Boolean,
      default: false,
    },
    silentOnInput: {
      type: Boolean,
      default: false,
    },
    spellcheck: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue", "validate"],
  computed: {
    classes() {
      return [
        this.element,
        this.sizeClass,
        this.invalid ? "is-danger" : this.colorClass,
        {
          "is-rounded": this.rounded,
          "is-loading": this.loading,
        },
      ];
    },
  },
  methods: {
    onInput(event) {
      this.$emit("update:modelValue", event.target.value);
      if (!this.silentOnInput) {
        this.emitValidate();
      }
    },
    emitValidate() {
      this.$emit("validate", this.name);
    },
  },
};
</script>