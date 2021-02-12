<template>
  <router-view />
</template>

<script>
import { useToast, TYPE } from "vue-toastification";
import { mapActions } from "vuex";
import { axios, apiRoutes } from "@/api";

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
      await this.initStore(); // Initialises global & user data (non-team sepecifc)
    } catch (err) {
      this.toast.error(
        `Failed to initialise team admin console: ${
          err.response?.data.detail ?? err
        }`
      );
    }
  },

  async mounted() {
    /* Creat toasts for any Django messages */
    const levelTagMap = {
      "is-danger": TYPE.ERROR,
      "is-success": TYPE.SUCCESS,
      "is-warning": TYPE.WARNING,
      "is-info": TYPE.INFO,
    };
    const response = await axios.get(apiRoutes.messages);
    const messages = response.data;
    if (messages.length) {
      messages.forEach((message) => {
        this.toast(message.message, { type: levelTagMap[message.levelTag] });
      });
    }
  },
};
</script>