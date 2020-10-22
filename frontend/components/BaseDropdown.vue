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
import bulmaDropdownMixin from "Mixins/bulmaDropdownMixin.js";

export default {
  mixins: [bulmaDropdownMixin],
  data() {
    return {
      isActive: false,
    };
  },
  computed: {
    classList() {
      return [
        "dropdown",
        {
          "is-hoverable": this.hoverable,
          "is-right": this.right,
          "is-up": this.up,
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
