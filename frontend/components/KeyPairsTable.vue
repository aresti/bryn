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
      <tr v-for="(keyPair, index) in keyPairs" :key="index">
        <td>
          <span class="has-text-weight-semibold">{{ keyPair.name }}</span
          ><br />
          <span class="is-size-7">
            {{ getRegionNameForTenant(getTenantById(keyPair.tenant)) }}</span
          >
        </td>
        <td class="is-family-monospace">{{ keyPair.fingerprint }}</td>
        <td>
          <div class="buttons is-right">
            <base-button
              rounded
              size="small"
              class="has-tooltip-left has-tooltip-multiline has-tooltip-text-left"
              :data-tooltip="keyPair.publicKey"
            >
              View Public Key
            </base-button>
            <base-button-delete
              size="small"
              @click="$emit('delete-keypair', keyPair)"
            />
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
    keyPairs: {
      type: Array,
      required: true,
    },
  },
  emits: {
    "delete-keypair": ({ id, name }) => {
      if (id && name) {
        return true;
      }
      console.warn("Invalid delete-keypair event payload");
      return false;
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