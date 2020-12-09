<template>
  <base-button color="success" fullwidth>
    <slot></slot>
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