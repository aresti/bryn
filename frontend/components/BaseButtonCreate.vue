<template>
  <base-button rounded color="success" :size="size"
    ><template v-slot:icon-before>
      <base-icon
        :size="size"
        :fa-classes="['fas', 'fa-plus-circle']"
        :decorative="true"
      />
    </template>
    <template v-slot:default><slot>New</slot></template>
  </base-button>
</template>

<script>
import BaseButton from "@/components/BaseButton";
import BaseIcon from "@/components/BaseIcon";
import bulmaSizeMixin from "@/mixins/bulmaSizeMixin";

export default {
  components: {
    BaseButton,
    BaseIcon,
  },
  mixins: [bulmaSizeMixin],
};
</script>