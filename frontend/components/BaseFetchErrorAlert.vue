<template>
  <base-alert context="danger">
    Sorry, something unexpected went wrong.
    <hr />
    Please try back later.
  </base-alert>
</template>

<script>
import BaseAlert from "@/components/BaseAlert";

export default {
  components: {
    BaseAlert,
  },
};
</script>
