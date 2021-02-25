<template>
  <div class="columns is-multiline">
    <div class="column is-half">
      <dashboard-tile routeName="servers">
        <dashboard-tile-metrics
          title="Servers"
          :metrics="{
            Servers: totalTeamInstances,
            vCPUs: totalTeamVCPUs,
            RAM: formatSize(totalTeamRamGb),
          }"
        />
      </dashboard-tile>
    </div>

    <div class="column is-half">
      <dashboard-tile routeName="volumes">
        <dashboard-tile-metrics
          title="Volumes"
          :metrics="{
            Volumes: totalTeamVolumes,
            Capacity: formatSize(totalTeamCapacity),
          }"
        />
      </dashboard-tile>
    </div>

    <div class="column is-half">
      <dashboard-tile routeName="teamManagement">
        <dashboard-tile-metrics
          title="Team"
          :metrics="{
            Members: allTeamMembers.length,
            Invitations: allInvitations.length,
          }"
        />
      </dashboard-tile>
    </div>

    <div class="column is-half">
      <dashboard-tile routeName="teamManagement">
        <dashboard-tile-licence />
      </dashboard-tile>
    </div>
  </div>
</template>

<script>
import { formatBytes } from "@/utils";

import { mapGetters } from "vuex";
import {
  ALL_INVITATIONS,
  ALL_TEAM_MEMBERS,
  TOTAL_TEAM_CAPACITY_GB,
  TOTAL_TEAM_INSTANCES,
  TOTAL_TEAM_RAM_GB,
  TOTAL_TEAM_VCPUS,
  TOTAL_TEAM_VOLUMES,
} from "@/store/getter-types";

import DashboardTile from "@/components/DashboardTile";
import DashboardTileLicence from "@/components/DashboardTileLicence";
import DashboardTileMetrics from "@/components/DashboardTileMetrics";

export default {
  components: {
    DashboardTile,
    DashboardTileLicence,
    DashboardTileMetrics,
  },

  computed: {
    ...mapGetters({
      allInvitations: ALL_INVITATIONS,
      allTeamMembers: ALL_TEAM_MEMBERS,
      totalTeamCapacity: TOTAL_TEAM_CAPACITY_GB,
      totalTeamInstances: TOTAL_TEAM_INSTANCES,
      totalTeamRamGb: TOTAL_TEAM_RAM_GB,
      totalTeamVCPUs: TOTAL_TEAM_VCPUS,
      totalTeamVolumes: TOTAL_TEAM_VOLUMES,
    }),
  },

  methods: {
    formatSize(gb) {
      return formatBytes(gb * Math.pow(1000, 3));
    },
  },
};
</script>