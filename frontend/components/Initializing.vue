<template>
  <base-hero-full centered>
    <h2 class="subtitle">Initializing team dashboard...</h2>
    <base-progress indeterminate color="success" />
  </base-hero-full>
</template>

<script>
import BaseHeroFull from "@/components/BaseHeroFull";
import BaseProgress from "@/components/BaseProgress";

export default {
  components: {
    BaseHeroFull,
    BaseProgress,
  },
};
</script>