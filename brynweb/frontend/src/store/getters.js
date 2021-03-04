import { createFindByIdGetter } from "@/utils/store";
import {
  ADMIN_TEAM_MEMBERS,
  DEFAULT_TENANT,
  FILTER_TENANT,
  LOADING,
  TEAM,
  TENANTS,
  USER_IS_ADMIN,
  USER_FULL_NAME,
  GET_TENANT_BY_ID,
  GET_REGION_BY_ID,
  GET_REGION_FOR_TENANT,
  GET_REGION_NAME_FOR_TENANT,
} from "./getter-types";

export const getters = {
  [USER_FULL_NAME](state) {
    return `${state.user.firstName} ${state.user.lastName}`;
  },
  [USER_IS_ADMIN](state, getters) {
    return getters[ADMIN_TEAM_MEMBERS].some(
      (member) => member.user.id === state.user.id
    );
  },
  [TEAM](state) {
    return state.teams.find((team) => team.id === state.activeTeamId);
  },
  [TENANTS](state, getters) {
    return state.activeTeamId
      ? getters[TEAM].tenants
          .filter((tenant) => {
            const region = getters[GET_REGION_FOR_TENANT](tenant);
            return !region.disabled; // Exclude tenants at disabled regions
          })
          .map((tenant) => {
            const region = getters[GET_REGION_FOR_TENANT](tenant);
            tenant.disableNewInstances = region.disableNewInstances; // Convenience disableNewInstances property
            return tenant;
          })
      : [];
  },
  [DEFAULT_TENANT](_state, getters) {
    return getters[TENANTS].find(
      (tenant) => tenant.region === getters[TEAM].defaultRegion
    );
  },
  [FILTER_TENANT](state, getters) {
    return getters[TENANTS].find(
      (tenant) => tenant.id === state.filterTenantId
    );
  },
  [GET_TENANT_BY_ID](_state, getters) {
    return createFindByIdGetter(getters[TENANTS]);
  },
  [GET_REGION_BY_ID](state) {
    return createFindByIdGetter(state.regions);
  },
  [GET_REGION_FOR_TENANT](_state, getters) {
    return (tenant) => getters[GET_REGION_BY_ID](tenant.region);
  },
  [GET_REGION_NAME_FOR_TENANT](_state, getters) {
    return (tenant) => {
      const region = getters[GET_REGION_FOR_TENANT](tenant);
      return region?.description?.replace("University of ", "");
    };
  },
  [LOADING](_state, getters) {
    return !getters[TEAM].initialized;
  },
};

export default getters;
