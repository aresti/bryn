<template>
  <tr class="is-size-6">
    <td>
      <span class="has-text-weight-semibold">{{ instance.name }}</span
      ><br />
      <span class="is-size-7">{{ regionName }}</span>
    </td>

    <td>
      {{ flavorName }}
    </td>

    <td>
      <base-tag-control>
        <base-tag v-if="isNew" color="dark" rounded>NEW</base-tag>
        <base-tag :color="statusColor" rounded light>
          {{ instance.status }}
          <base-icon
            v-if="isPolling"
            class="ml-1"
            :fa-classes="['fas', 'fa-spinner', 'fa-spin']"
            :decorative="true"
          />
        </base-tag>
      </base-tag-control>
      <span class="is-family-monospace is-size-7">{{ instance.ip }}</span>
    </td>

    <td>{{ timeSinceCreated }}</td>

    <td class="actions-cell">
      <base-buttons v-if="!isPolling" class="is-right">
        <base-button
          v-for="action in stateTransitionActions"
          :key="action"
          :color="action.color"
          size="small"
          outlined
          rounded
          @click="onActionClick(action)"
        >
          {{ action.verb }}
        </base-button>
      </base-buttons>
    </td>
  </tr>

  <!-- Confirm action modal -->
  <base-modal-delete
    v-if="confirmAction"
    :verb="confirmAction.verb"
    type="server"
    :name="instance.name"
    :processing="actionProcessing"
    @close-modal="onCancelAction"
    @confirm-delete="onConfirmAction"
  />
</template>

<script>
import { minutesSince } from "@/utils";
import { formatDistanceToNow } from "date-fns";
import { mapActions, mapGetters } from "vuex";

const statusColorMap = {
  ACTIVE: "success",
  SHUTDOWN: "grey-light",
  SHELVED: "grey-lighter",
};

/*
 * State transitions
 * Top level is current status, 1st level is target status
 */
const stateTransitions = {
  ACTIVE: [
    {
      targetStatus: "ACTIVE",
      verb: "Reboot",
      presentParticiple: "Rebooting",
      color: "warning",
      confirm: true,
    },
    {
      targetStatus: "SHUTOFF",
      verb: "Stop",
      presentParticiple: "Stopping",
      color: "danger",
      confirm: true,
    },
  ],
  SHUTOFF: [
    {
      targetStatus: "ACTIVE",
      verb: "Start",
      presentParticiple: "Starting",
      color: "success",
      confirm: false,
    },
    {
      targetStatus: "DELETED",
      verb: "Delete",
      presentParticiple: "Deleting",
      color: "danger",
      confirm: true,
    },
  ],
  SHELVED: [
    {
      targetStatus: "SHUTOFF",
      verb: "Unshelve",
      presentParticiple: "Unshelving",
      color: "info",
      confirm: false,
    },
  ],
};

export default {
  // Composition
  inject: ["toast"],

  // Interface
  props: {
    instance: {
      type: Object,
      required: true,
    },
  },

  // Local state
  data() {
    return {
      confirmAction: null,
      actionProcessing: false,
    };
  },

  computed: {
    ...mapGetters(["getTenantById", "getRegionNameForTenant"]),
    ...mapGetters("flavors", ["getFlavorById"]),
    ...mapGetters("instances", ["getInstanceIsPolling"]),
    isNew() {
      return minutesSince(this.instance.created) < 3;
    },
    isPolling() {
      return this.getInstanceIsPolling(this.instance);
    },
    regionName() {
      const tenant = this.getTenantById(this.instance.tenant);
      return this.getRegionNameForTenant(tenant);
    },
    flavorName() {
      return (
        this.getFlavorById(this.instance.flavor)?.name ?? "[legacy flavor]"
      );
    },
    timeSinceCreated() {
      return formatDistanceToNow(new Date(this.instance.created)) + " ago";
    },
    statusColor() {
      const { [this.instance.status]: color } = statusColorMap;
      return color;
    },
    stateTransitionActions() {
      return stateTransitions[this.instance.status];
    },
  },

  // Non-reactive
  methods: {
    ...mapActions("instances", [
      "deleteInstance",
      "fetchInstance",
      "targetInstanceStatus",
    ]),

    onActionClick(action) {
      if (action.confirm) {
        this.confirmAction = action;
      } else {
        this.performAction(action);
      }
    },

    onCancelAction() {
      this.confirmAction = null;
    },

    async onConfirmAction() {
      await this.performAction(this.confirmAction);
      this.confirmAction = null;
    },

    async performAction(action) {
      if (this.actionProcessing) {
        return;
      }
      this.actionProcessing = true;
      const toastMsg = `${action.presentParticiple} ${this.instance.name}`;
      try {
        if (action.color == "success") {
          this.toast.success(toastMsg);
        } else {
          this.toast(toastMsg);
        }
        if (action.targetStatus === "DELETED") {
          await this.deleteInstance(this.instance);
        } else {
          await this.targetInstanceStatus({
            instance: this.instance,
            status: action.targetStatus,
          });
        }
      } catch (err) {
        this.toast.error(
          `Failed to ${action.verb} ${this.instance.name}: ${
            err.response?.data.detail ?? "unexpected error"
          }`
        );
      } finally {
        this.actionProcessing = false;
      }
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