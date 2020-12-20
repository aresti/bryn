<template>
  <base-table fullwidth hoverable>
    <template v-slot:head>
      <tr>
        <th v-for="heading in headings" :key="heading">
          {{ heading }}
        </th>
      </tr>
    </template>
    <template v-slot:body>
      <tr v-for="(volume, index) in volumes" :key="index">
        <td>
          <span class="has-text-weight-semibold">{{ volume.name }}</span>
          <br />
          <span class="is-size-7">
            {{ getRegionNameForTenant(getTenantById(volume.tenant)) }}</span
          >
        </td>
        <td>
          <span class="has-text-weight-semibold">{{ volume.volumeType }}</span
          ><br />
          <span v-if="volume.bootable" class="is-size-7">Bootable</span>
        </td>
        <td>{{ formatSize(volume.size) }}</td>
        <td>
          <div class="control">
            <div class="tags has-addons">
              <base-tag v-if="isNew(volume)" color="dark" rounded>New</base-tag>
              <base-tag :color="statusColor(volume.status)" rounded light>
                {{ volume.status }}
                <base-icon
                  v-if="getVolumeIsPolling(volume)"
                  class="ml-1"
                  :fa-classes="['fas', 'fa-spinner', 'fa-spin']"
                  :decorative="true"
                />
              </base-tag>
            </div>
          </div>
        </td>
        <td>
          <span
            v-for="attachment in formatAttachments(volume.attachments)"
            :key="attachment.id"
          >
            {{ attachment.attachedToName }}<br />
            <span class="is-family-monospace is-size-7">{{
              attachment.device
            }}</span>
          </span>
        </td>
        <td>
          <div class="buttons is-right">
            <base-button-delete size="small" />
          </div>
        </td>
      </tr>
    </template>
  </base-table>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { formatBytes, minutesSince } from "@/utils";

export default {
  props: {
    volumes: {
      type: Array,
      required: true,
    },
  },

  data() {
    return {
      headings: ["Name", "Volume Type", "Size", "Status", "Attached To", ""],
    };
  },

  computed: {
    ...mapGetters(["getRegionNameForTenant", "getTenantById"]),
    ...mapGetters("instances", ["getInstanceById"]),
    ...mapGetters("volumes", ["getVolumeIsPolling"]),
  },

  methods: {
    isNew(volume) {
      return minutesSince(volume.createdAt) < 3;
    },
    formatAttachments(attachments) {
      return attachments.map((attachment) => {
        return {
          attachedToName: this.getInstanceById(attachment.serverId)?.name,
          device: attachment.device,
        };
      });
    },
    formatSize(size) {
      return formatBytes(size * Math.pow(1000, 3));
    },
    statusColor(status) {
      const colors = {
        "in-use": "success",
        available: "info",
      };
      const color = colors[status];
      return color;
    },
  },
};
</script>

<style scoped>
td {
  vertical-align: middle;
}

.actions-cell {
  text-align: right;
}
</style>