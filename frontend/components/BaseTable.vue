<template>
  <table :class="classes">
    <thead>
      <slot name="head"></slot>
    </thead>
    <tbody>
      <slot name="body"></slot>
    </tbody>
  </table>
</template>

<script>
export default {
  props: {
    fullwidth: {
      type: Boolean,
      required: false,
    },
    hoverable: {
      type: Boolean,
      required: false,
    },
    striped: {
      type: Boolean,
      required: false,
    },
  },
  computed: {
    classes() {
      return [
        "table",
        {
          "is-fullwidth": this.fullwidth,
          "is-hoverable": this.hoverable,
          "is-striped": this.striped,
        },
      ];
    },
  },
};
</script>