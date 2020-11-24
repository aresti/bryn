<template>
  <base-hero-full centered>
    <h2 class="subtitle">404 Not Found</h2>
    <p>Sorry, there's nothing here!</p>
  </base-hero-full>
</template>

<script>
import BaseHeroFull from "@/components/BaseHeroFull";
import { mapState } from "vuex";

export default {
  components: {
    BaseHeroFull,
  },
};
</script>