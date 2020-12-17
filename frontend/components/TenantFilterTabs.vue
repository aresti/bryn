<template>
  <base-tabs toggle rounded>
    <li :class="{ 'is-active': filterTenantId == null }">
      <a @click="onTabClick">All</a>
    </li>
    <li
      v-for="tenant in tenants"
      :key="tenant.id"
      :class="{ 'is-active': tenant.id === filterTenantId }"
    >
      <a @click="onTabClick(tenant)">{{ getRegionNameForTenant(tenant) }}</a>
    </li>
  </base-tabs>
</template>

<script>
import { mapGetters, mapActions, mapState } from "vuex";

export default {
  computed: {
    ...mapState(["filterTenantId"]),
    ...mapGetters(["tenants", "getRegionNameForTenant"]),
  },
  methods: {
    ...mapActions(["setFilterTenant"]),
    onTabClick(tenant = null) {
      this.setFilterTenant(tenant);
    },
  },
};
</script>