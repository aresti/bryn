<template>
  <router-view />
</template>

<script>
import { useToast } from "vue-toastification";
import { mapActions } from "vuex";

export default {
  // Composition
  provide() {
    return {
      toast: this.toast, // Global toast interface
    };
  },

  // Composition API
  setup() {
    const toast = useToast();
    return { toast };
  },

  // Local state
  computed: mapActions(["initStore"]),

  // Events
  async beforeMount() {
    try {
      const keypair = await this.initStore();
    } catch (err) {
      this.toast.error(
        `Failed to initialise dashboard: ${err.response?.data.detail ?? err}`
      );
    }
  },
};
</script>