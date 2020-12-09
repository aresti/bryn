<template>
  <base-tabs toggle rounded>
    <li :class="{ 'is-active': filterTenant == null }">
      <a @click="onTabClick">All</a>
    </li>
    <li
      v-for="tenant in tenants"
      :key="tenant.id"
      :class="{ 'is-active': tenant.id === filterTenant }"
    >
      <a @click="onTabClick(tenant)">{{ getRegionNameForTenant(tenant) }}</a>
    </li>
  </base-tabs>
</template>

<script>
import BaseTabs from "@/components/BaseTabs";
import { mapGetters, mapMutations, mapState } from "vuex";

export default {
  components: { BaseTabs },
  computed: {
    ...mapState(["filterTenant"]),
    ...mapGetters(["tenants", "getRegionNameForTenant"]),
  },
  methods: {
    ...mapMutations(["setFilterTenant"]),
    onTabClick(tenant = null) {
      this.setFilterTenant(tenant);
    },
  },
};
</script>