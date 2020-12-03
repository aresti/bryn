<template>
  <option :disabled="disabled" :value="tenant.id">
    {{ valueDisplay }}
  </option>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    tenant: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters(["getRegionById"]),
    region() {
      return this.getRegionById(this.tenant.region);
    },
    disabled() {
      return this.region.disabled || this.region.disableNewInstances;
    },
    valueDisplay() {
      return this.region.description + (this.disabled ? " (disabled)" : "");
    },
  },
};
</script>