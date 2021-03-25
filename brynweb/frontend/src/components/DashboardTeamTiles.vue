<template>
  <div class="columns is-mobile">
    <div
      v-for="(obj, key) in tiles"
      :key="key"
      class="column"
      :class="{ 'is-hidden-mobile': !obj.mobile }"
    >
      <dashboard-stats-tile
        :description="key"
        :iconClasses="obj.iconClasses"
        :data="String(obj.value)"
      />
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

import DashboardStatsTile from "@/components/DashboardStatsTile";

export default {
  components: {
    DashboardStatsTile,
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
    tiles() {
      return {
        Servers: {
          iconClasses: ["fas", "server"],
          value: this.totalTeamInstances,
          mobile: true,
        },
        vCPUs: {
          iconClasses: ["fas", "microchip"],
          value: this.totalTeamVCPUs,
          mobile: true,
        },
        Memory: {
          iconClasses: ["fas", "memory"],
          value: formatBytes(this.totalTeamRamGb * Math.pow(1000, 3)),
          mobile: false,
        },
        Volumes: {
          iconClasses: ["fas", "hdd"],
          value: this.totalTeamVolumes,
          mobile: true,
        },
        Storage: {
          iconClasses: ["fas", "box"],
          value: formatBytes(this.totalTeamCapacity * Math.pow(1000, 3)),
          mobile: false,
        },
      };
    },
  },

  methods: {
    formatSize(gb) {
      return formatBytes(gb * Math.pow(1000, 3));
    },
  },
};
</script>