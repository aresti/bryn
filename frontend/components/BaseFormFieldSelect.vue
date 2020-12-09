<template>
  <div :class="wrapperClasses">
    <select
      :name="name"
      :value="modelValue"
      @change="onChange"
      :class="selectClasses"
    >
      <option value="" disabled>{{ nullOptionLabel }}</option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
        :disabled="option.disabled"
      >
        {{ option.label }}
      </option>
    </select>
  </div>
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
    options: {
      type: Array,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    nullOptionLabel: {
      type: String,
      default: "Select an option",
    },
    invalid: {
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
  },
  emits: ["update:modelValue", "validate"],
  computed: {
    wrapperClasses() {
      return [
        "select",
        {
          "is-rounded": this.rounded,
        },
      ];
    },
    selectClasses() {
      return [
        this.sizeClass,
        this.invalid ? "is-danger" : this.colorClass,
        {
          "is-loading": this.loading,
        },
      ];
    },
  },
  methods: {
    onChange(event) {
      this.$emit("update:modelValue", event.target.value), this.emitValidate();
    },
    emitValidate() {
      this.$emit("validate", this.name);
    },
  },
};
</script>  