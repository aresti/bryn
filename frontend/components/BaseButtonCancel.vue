<template>
  <base-button>
    <slot>Cancel</slot>
  </base-button>
</template>

<script>
import BaseButton from "@/components/BaseButton";

export default {
  components: {
    BaseButton,
  },
};
</script>