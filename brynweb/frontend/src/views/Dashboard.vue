<template>
  <div class="columns is-relative is-variable is-5">
    <div class="column is-8">
      <dashboard-team-tiles />
      <dashboard-service-status />
    </div>

    <div class="column is-4 announcements-column">
      <dashboard-announcements />
    </div>
  </div>
</template>

<script>
import DashboardAnnouncements from "@/components/DashboardAnnouncements.vue";
import DashboardServiceStatus from "@/components/DashboardServiceStatus.vue";
import DashboardTeamTiles from "@/components/DashboardTeamTiles.vue";

export default {
  components: {
    DashboardAnnouncements,
    DashboardServiceStatus,
    DashboardTeamTiles,
  },
};
</script>

<style lang="scss" scoped>
.announcements-column {
  border-left: 1px solid hsl(0, 0%, 90%);
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
}
</style>