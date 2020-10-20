<template>
  <nav class="tabs is-boxed is-fullwidth">
    <div class="container">
      <ul>
        <li
          v-for="(name, key) in tabs"
          :key="key"
          :class="{ 'is-active': currentTab === key }"
        >
          <a href="#" @click="selectTab(key)">
            {{ name }}
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  props: {
    tabs: {
      type: Object,
      required: true,
    },
    currentTab: {
      type: String,
      required: true,
    },
  },
  emits: {
    tabSelected: (key) => {
      if (key) {
        return true;
      } else {
        console.warn("Invalid tabSelected event payload!");
        return false;
      }
    },
  },
  methods: {
    selectTab(key) {
      this.$emit("tabSelected", key);
    },
  },
};
</script>