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
          {{ volume.volumeType }}<br />
          <span v-if="volume.bootable" class="is-size-7">Bootable</span>
        </td>

        <td>{{ formatSize(volume.size) }}</td>

        <td>
          <base-tag-control>
            <base-tag v-if="isNew(volume)" color="dark" rounded>NEW</base-tag>
            <base-tag :color="statusColor(volume.status)" rounded light>
              {{ volume.status.toUpperCase() }}
              <base-icon
                v-if="getVolumeIsPolling(volume)"
                class="ml-1"
                :fa-classes="['fas', 'fa-spinner', 'fa-spin']"
                :decorative="true"
              />
            </base-tag>
          </base-tag-control>
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

        <td class="is-size-6">{{ timeSinceCreated(volume) }}</td>

        <td>
          <div class="buttons is-right">
            <base-button
              v-if="isAvailable(volume)"
              size="small"
              color="success"
              outlined
              rounded
            >
              <template v-slot:default>Mount</template>
              <template v-slot:icon-before>
                <base-icon
                  :fa-classes="['fas', 'fa-link']"
                  :decorative="true"
                />
              </template>
            </base-button>
            <base-button v-if="isInUse(volume)" size="small" outlined rounded>
              <template v-slot:default>Unmount</template>
              <template v-slot:icon-before>
                <base-icon
                  :fa-classes="['fas', 'fa-unlink']"
                  :decorative="true"
                />
              </template>
            </base-button>
            <base-button-delete
              v-if="isAvailable(volume)"
              size="small"
              @click="$emit('delete-volume', volume)"
            />
          </div>
        </td>
      </tr>
    </template>
  </base-table>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { formatBytes, minutesSince } from "@/utils";
import { formatDistanceToNow } from "date-fns";

export default {
  props: {
    volumes: {
      type: Array,
      required: true,
    },
  },

  emits: {
    "delete-volume": ({ id, name }) => {
      if (id && name) {
        return true;
      }
      console.warn("Invalid delete-volume event payload");
      return false;
    },
  },

  data() {
    return {
      headings: [
        "Name",
        "Type",
        "Size",
        "Status",
        "Attached To",
        "Created",
        "",
      ],
    };
  },

  computed: {
    ...mapGetters(["getRegionNameForTenant", "getTenantById"]),
    ...mapGetters("instances", ["getInstanceById"]),
    ...mapGetters("volumes", ["getVolumeIsPolling"]),
  },

  methods: {
    isNew(volume) {
      return minutesSince(volume.createdAt) < 3 && !this.isDeleting(volume);
    },
    isAvailable(volume) {
      return volume.status === "available";
    },
    isInUse(volume) {
      return volume.status === "in-use";
    },
    isDeleting(volume) {
      return volume.status === "deleting";
    },
    timeSinceCreated(volume) {
      return formatDistanceToNow(new Date(volume.createdAt)) + " ago";
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