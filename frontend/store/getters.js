import { createFilterByIdGetter } from "@/utils/store";

export const getters = {
  userFullName(state) {
    return `${state.user.firstName} ${state.user.lastName}`;
  },
  team(state) {
    return state.teams.find((team) => team.id === state.activeTeamId);
  },
  tenants(state, getters) {
    return state.activeTeamId ? getters.team.tenants : [];
  },
  defaultTenant(_state, getters) {
    return getters.tenants.find(
      (tenant) => tenant.region === getters.team.defaultRegion
    );
  },
  filterTenant(state, getters) {
    return getters.tenants.find((tenant) => tenant.id === state.filterTenantId);
  },
  getTenantById(_state, getters) {
    return createFilterByIdGetter(getters.tenants);
  },
  getRegionById(state) {
    return createFilterByIdGetter(state.regions);
  },
  getRegionNameForTenant(_state, getters) {
    return (tenant) => {
      const region = getters.getRegionById(tenant.region);
      return region?.description?.replace("University of ", "");
    };
  },
  loading(_state, getters) {
    return !getters.team.initialized;
  },
};

export default getters;
