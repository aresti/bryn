<template>
  <div class="box">
    <article class="media">
      <div class="media-content">
        <div class="content">
          <strong>{{ announcement.title }}</strong>
          <div class="mt-2" v-html="announcement.content"></div>
          <span class="is-size-7 is-italic mt-1">{{ createdAt }}</span>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
import { formatRelative } from "date-fns";

export default {
  props: {
    announcement: {
      type: Object,
      required: true,
    },
  },

  computed: {
    createdAt() {
      return formatRelative(new Date(this.announcement.createdAt), new Date());
    },
  },
};
</script>