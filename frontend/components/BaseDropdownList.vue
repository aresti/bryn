<template>
  <base-dropdown :hoverable="hoverable" :right="right" :up="up">
    <template v-slot:trigger="{ toggle: toggleDropdown }">
      <base-button
        @click="toggleDropdown"
        rounded
        dropdown
        outlined
        color="white"
      >
        <slot name="title"></slot>
      </base-button>
    </template>
    <template v-slot="{ toggle: toggleDropdown }">
      <a
        v-for="item in items"
        :key="item"
        @click="
          toggleDropdown();
          selectItem(item);
        "
        class="dropdown-item"
        :class="{
          'is-active': item == activeItem,
          'has-text-weight-bold': item == activeItem,
        }"
      >
        <slot name="item" :item="item"></slot>
      </a>
    </template>
  </base-dropdown>
</template>

<script>
import BaseButton from "./BaseButton.vue";
import BaseDropdown from "./BaseDropdown.vue";

import bulmaDropdownMixin from "Mixins/bulmaDropdownMixin.js";

export default {
  mixins: [bulmaDropdownMixin],
  components: {
    BaseButton,
    BaseDropdown,
  },
  props: {
    items: {
      type: Array,
      required: true,
    },
    activeItem: {
      type: Object,
      required: true,
    },
  },
  methods: {
    selectItem(item) {
      this.$emit("itemSelected", item);
    },
  },
  emits: {
    itemSelected: null,
  },
};
</script>