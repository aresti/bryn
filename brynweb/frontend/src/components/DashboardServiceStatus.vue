<template>
  <div class="box">
    <h3 class="subtitle">Service status</h3>
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <th>Region</th>
          <th>Capacity?</th>
          <th>VMs</th>
          <th class="has-text-centered">vCPUs</th>
          <th class="has-text-centered">Memory</th>
          <th class="has-text-centered is-hidden-mobile">Storage</th>
        </tr>
      </thead>
      <tbody>
        <dashboard-service-status-row
          v-for="stats in hypervisorStats"
          :key="stats.region"
          :stats="stats"
        />
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapState } from "vuex";
import DashboardServiceStatusRow from "@/components/DashboardServiceStatusRow";

export default {
  components: {
    DashboardServiceStatusRow,
  },

  computed: {
    ...mapState({
      hypervisorStats: (state) => state.hypervisorStats,
    }),
  },
};
</script>