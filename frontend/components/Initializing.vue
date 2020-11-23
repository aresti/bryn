<template>
  <base-hero-full centered>
    <h2 class="subtitle">Initializing team dashboard...</h2>
    <base-progress indeterminate color="success" />
  </base-hero-full>
</template>

<script>
import BaseHeroFull from "@/components/BaseHeroFull.vue";
import BaseProgress from "@/components/BaseProgress.vue";

export default {
  components: {
    BaseHeroFull,
    BaseProgress,
  },
};
</script>