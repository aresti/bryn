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
      <tr v-for="keypair in keypairs" :key="keypair.id">
        <td>
          <span class="is-family-monospace has-text-weight-semibold">{{
            keypair.name
          }}</span
          ><br />
          <span class="is-size-7">
            {{ getRegionNameForTenant(getTenantById(keypair.tenant)) }}</span
          >
        </td>
        <td class="is-family-monospace">{{ keypair.fingerprint }}</td>
        <td>
          <div class="buttons is-right">
            <base-button
              rounded
              size="small"
              class="has-tooltip-left has-tooltip-multiline has-tooltip-text-left"
              :data-tooltip="keypair.publicKey"
            >
              View Public Key
            </base-button>
            <base-button-delete size="small" />
          </div>
        </td>
      </tr>
    </template>
  </base-table>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    keypairs: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      headings: ["Name", "Fingerprint", ""],
    };
  },
  computed: {
    ...mapGetters(["getRegionNameForTenant", "getTenantById"]),
  },
};
</script>

<style scoped>
[data-tooltip]:not(.is-loading).has-tooltip-multiline::before,
[data-tooltip]:not(.is-disabled).has-tooltip-multiline::before,
[data-tooltip]:not([disabled]).has-tooltip-multiline::before {
  overflow-wrap: anywhere;
  width: 25em;
  max-width: 25em;
}

td {
  vertical-align: middle;
}
</style>