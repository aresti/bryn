<template>
  <router-view />
</template>

<script>
export default {
  beforeMount() {
    this.$store.dispatch("initStore");
  },
};
</script>