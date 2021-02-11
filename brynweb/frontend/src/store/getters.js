import { createFindByIdGetter } from "@/utils/store";

export const getters = {
  userFullName(state) {
    return `${state.user.firstName} ${state.user.lastName}`;
  },
  userIsAdmin(state, getters) {
    return getters["teamMembers/adminTeamMembers"].some(
      (member) => member.user.id === state.user.id
    );
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
    return createFindByIdGetter(getters.tenants);
  },
  getRegionById(state) {
    return createFindByIdGetter(state.regions);
  },
  getRegionForTenant(_state, getters) {
    return (tenant) => getters.getRegionById(tenant.region);
  },
  getRegionNameForTenant(_state, getters) {
    return (tenant) => {
      const region = getters.getRegionForTenant(tenant);
      return region?.description?.replace("University of ", "");
    };
  },
  loading(_state, getters) {
    return !getters.team.initialized;
  },
};

export default getters;
