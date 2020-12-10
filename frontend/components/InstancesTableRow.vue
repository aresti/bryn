<template>
  <tr class="is-size-6">
    <td>
      <base-icon
        :fa-classes="['fas', 'fa-circle']"
        class="mr-2"
        :color="statusColor"
      />
    </td>
    <td>
      <span class="is-family-monospace has-text-weight-semibold">{{
        instance.name
      }}</span
      ><br />
      <span class="is-size-7">{{ regionName }}</span>
    </td>
    <td>
      {{ flavorName }}
    </td>
    <td>
      <base-tag :color="statusColor" rounded light>{{
        instance.status
      }}</base-tag
      ><br />
      <span class="is-family-monospace is-size-7">{{ instance.ip }}</span>
    </td>
    <td>{{ createdDistanceToNow }}</td>
    <td class="actions-cell">
      <base-dropdown right>
        <template v-slot:trigger="{ toggle: toggleDropdown }">
          <base-button @click="toggleDropdown" dropdown outlined>
            Actions
          </base-button>
        </template>
        <template v-slot="{ toggle: toggleDropdown }">
          <a @click="toggleDropdown" class="dropdown-item"> Test </a>
        </template>
      </base-dropdown>
    </td>
  </tr>
</template>

<script>
import { formatDistanceToNow } from "date-fns";

import { mapGetters } from "vuex";

const statusColorMap = {
  ACTIVE: "success",
  SHUTDOWN: "grey-light",
  SHELVED: "grey-lighter",
};

export default {
  props: {
    instance: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters(["getRegionNameForTenant", "getTenantById"]),
    ...mapGetters("flavors", ["getFlavorById"]),
    tenant() {
      return this.getTenantById(this.instance.tenant);
    },
    regionName() {
      return this.getRegionNameForTenant(this.tenant);
    },
    flavorName() {
      return (
        this.getFlavorById(this.instance.flavor)?.name ?? "[legacy flavor]"
      );
    },
    createdDistanceToNow() {
      return formatDistanceToNow(new Date(this.instance.created)) + " ago";
    },
    statusColor() {
      const { [this.instance.status]: color } = statusColorMap;
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