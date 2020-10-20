<template>
  <button @click="click" :class="classList" :disabled="disabled">
    <slot name="icon-before"></slot>

    <span>
      <slot></slot>
    </span>

    <slot name="icon-after">
      <span v-if="dropdown" class="icon is-small">
        <i class="fas fa-angle-down" aria-hidden="true"></i>
      </span>
    </slot>
  </button>
</template>

<script>
export default {
  emits: {
    click: null,
  },
  props: {
    size: {
      type: String,
      default: "normal",
      validator: function (value) {
        return ["small", "normal", "medium", "large"].indexOf(value) !== -1;
      },
    },
    color: {
      type: String,
      required: false,
      default: "",
      validator: function (value) {
        return (
          [
            "",
            "white",
            "light",
            "dark",
            "black",
            "text",
            "primary",
            "link",
            "success",
            "warning",
            "danger",
            "info",
          ].indexOf(value) !== -1
        );
      },
    },
    light: {
      type: Boolean,
      default: false,
    },
    rounded: {
      type: Boolean,
      default: false,
    },
    fullwidth: {
      type: Boolean,
      default: false,
    },
    outlined: {
      type: Boolean,
      default: false,
    },
    inverted: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    dropdown: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    colorClass() {
      if (this.color) {
        return "is-" + this.color;
      }
    },
    sizeClass() {
      if (this.size) {
        return "is-" + this.size;
      }
    },
    classList() {
      return [
        "button",
        this.colorClass,
        this.sizeClass,
        {
          "is-light": this.light,
          "is-rounded": this.rounded,
          "is-fullwidth": this.fullwidth,
          "is-outlined": this.outlined,
          "is-inverted": this.inverted,
          "is-loading": this.loading,
        },
      ];
    },
  },
  methods: {
    click() {
      if (!this.disabled) {
        this.$emit("click");
      }
    },
  },
};
</script>
