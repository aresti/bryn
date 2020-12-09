<template>
  <base-modal>
    <base-card>
      <div class="columns is-variable is-5">
        <div class="column is-7 content" ref="leftCol">
          <slot name="left"></slot>
        </div>
        <div
          class="column is-5 content modal-right-col"
          :style="rightInlineStyle"
        >
          <slot name="right"></slot>
        </div>
      </div>
    </base-card>
  </base-modal>
</template>

<script>
import BaseCard from "@/components/BaseCard";
import BaseModal from "@/components/BaseModal";

export default {
  data() {
    return {
      leftHeightPx: null,
    };
  },
  components: {
    BaseCard,
    BaseModal,
  },
  computed: {
    rightInlineStyle() {
      return this.leftHeightPx == null ? "" : `height: ${this.leftHeightPx}px`;
    },
  },
  methods: {
    matchHeight() {
      this.leftHeightPx = this.$refs.leftCol.clientHeight;
    },
  },
  mounted() {
    this.matchHeight();
  },
};
</script>

<style scoped>
.modal-right-col {
  border-left: 1px solid hsl(0, 0%, 96%);
  overflow-y: auto;
}
</style>