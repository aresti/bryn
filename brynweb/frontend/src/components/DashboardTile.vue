<template>
  <base-notification
    @click="onClick"
    @mouseover="hover = true"
    @mouseleave="hover = false"
    @hover="hover = true"
    :color="color"
    class="tile-link"
  >
    <slot></slot>
  </base-notification>
</template>

<script>
import { mapGetters } from "vuex";
import { TEAM } from "@/store/getter-types";

export default {
  props: {
    routeName: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      hover: false,
    };
  },

  computed: {
    ...mapGetters({
      team: TEAM,
    }),
    color() {
      return this.hover ? "primary" : undefined;
    },
  },

  methods: {
    onClick() {
      this.hover = false;
      this.$router.push({
        name: this.routeName,
        params: { teamId: this.team.id },
      });
    },
  },
};
</script>

<style scoped>
.tile-link {
  cursor: pointer;
}
</style>