<template>
  <base-button rounded color="success" :size="size" outlined
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
import bulmaSizeMixin from "@/mixins/bulmaSizeMixin";

export default {
  mixins: [bulmaSizeMixin],
};
</script>