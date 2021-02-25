<template>
  <tr>
    <td>
      <span class="icon-text">
        <base-icon
          :icon="['fas', region.disabled ? 'times-circle' : 'check-circle']"
          :decorative="true"
        />
        <span>{{ region.name }}</span>
      </span>
    </td>
    <td>{{ stats.runningVms }}</td>
    <td>
      <p class="is-size-7 has-text-centered">
        {{ stats.vcpusUsed }} / {{ stats.vcpus }}
      </p>
      <base-progress :value="vcpusPercent" :max="100" color="info" />
    </td>
    <td>
      <p class="is-size-7 has-text-centered">
        {{ MBtoTB(stats.memoryMbUsed) }} / {{ MBtoTB(stats.memoryMb) }} TB
      </p>
      <base-progress :value="memoryPercent" :max="100" color="info" />
    </td>
    <td>
      <p class="is-size-7 has-text-centered">
        {{ GBtoPB(stats.localGbUsed) }} / {{ GBtoPB(stats.localGb) }} PB
      </p>
      <base-progress :value="localGbPercent" :max="100" color="info" />
    </td>
  </tr>
</template>

<script>
import { mapGetters } from "vuex";
import { GET_REGION_BY_ID } from "@/store/getter-types";

export default {
  props: {
    stats: {
      type: Object,
      required: true,
    },
  },

  computed: {
    ...mapGetters({
      getRegionById: GET_REGION_BY_ID,
    }),
    region() {
      return this.getRegionById(this.stats.region);
    },
    localGbPercent() {
      return Math.round((this.stats.localGbUsed / this.stats.localGb) * 100);
    },
    memoryPercent() {
      return Math.round((this.stats.memoryMbUsed / this.stats.memoryMb) * 100);
    },
    vcpusPercent() {
      return Math.round((this.stats.vcpusUsed / this.stats.vcpus) * 100);
    },
  },

  methods: {
    MBtoTB(mb) {
      return (mb / Math.pow(1000, 2)).toFixed(1);
    },
    GBtoPB(gb) {
      return (gb / Math.pow(1000, 2)).toFixed(1);
    },
  },
};
</script>

<style scoped>
td {
  vertical-align: middle;
}
</style>