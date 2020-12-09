<template>
  <base-button rounded color="danger" :size="size" outlined
    ><template v-slot:icon-before>
      <base-icon
        :size="size"
        :fa-classes="['fas', 'fa-trash-alt']"
        :decorative="true"
      />
    </template>
    <template v-slot:default><slot>Delete</slot></template>
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