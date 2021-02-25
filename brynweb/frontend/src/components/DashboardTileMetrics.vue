<template>
  <p class="title has-text-centered is-size-4">{{ title }}</p>
  <div class="level">
    <div
      v-for="(value, label) in metrics"
      :key="label"
      class="level-item has-text-centered"
    >
      <div>
        <p class="heading">{{ label }}</p>
        <p class="title">{{ value }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },

    metrics: {
      type: Object,
      required: true,
    },
  },
};
</script>