<template>
  <div class="icon-text mb-2">
    <base-icon size="large" :icon="['fas', 'bullhorn']" :decorative="true" />
    <span class="mt-3 is-size-5">News & Announcements</span>
  </div>
  <service-announcement
    v-for="announcement in serviceAnnouncements"
    :key="announcement.id"
    :announcement="announcement"
  />
  <news-announcement
    v-for="announcement in newsAnnouncements"
    :key="announcement.id"
    :announcement="announcement"
  />
</template>

<script>
import { mapGetters } from "vuex";
import {
  NEWS_ANNOUNCEMENTS,
  SERVICE_ANNOUNCEMENTS,
} from "@/store/getter-types";

import NewsAnnouncement from "@/components/NewsAnnouncement";
import ServiceAnnouncement from "@/components/ServiceAnnouncement";

export default {
  components: {
    NewsAnnouncement,
    ServiceAnnouncement,
  },

  computed: {
    ...mapGetters({
      newsAnnouncements: NEWS_ANNOUNCEMENTS,
      serviceAnnouncements: SERVICE_ANNOUNCEMENTS,
    }),
  },
};
</script>