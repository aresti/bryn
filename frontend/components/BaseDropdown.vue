<template>
  <div :class="classList">
    <div class="dropdown-trigger">
      <slot name="trigger" :toggle="toggle"></slot>
    </div>
    <div class="dropdown-menu" role="menu">
      <div class="dropdown-content">
        <slot :toggle="toggle"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isActive: false,
    };
  },
  props: {
    hoverable: {
      type: Boolean,
    },
    right: {
      type: Boolean,
    },
  },
  computed: {
    classList() {
      return [
        "dropdown",
        {
          "is-hoverable": this.hoverable,
          "is-right": this.right,
          "is-active": this.isActive,
        },
      ];
    },
  },
  methods: {
    toggle() {
      if (!this.hoverable) {
        this.isActive = !this.isActive;
      }
    },
  },
};
</script>
