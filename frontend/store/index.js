import { createStore } from "vuex";
import { createFilterByIdGetter } from "@/utils";

import flavors from "./modules/flavors";
import images from "./modules/images";
import instances from "./modules/instances";
import keyPairs from "./modules/keyPairs";
import teamMembers from "./modules/teamMembers";
import volumes from "./modules/volumes";
import volumeTypes from "./modules/volumeTypes";

const state = {
  adminEmail: "Lisa.Marchioretto@quadram.ac.uk",
  activeTeamId: null,
  filterTenantId: null,
  regions: [],
  teams: [],
  user: null,
};

const modules = {
  flavors,
  images,
  instances,
  keyPairs,
  teamMembers,
  volumes,
  volumeTypes,
};

const getters = {
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

const mutations = {
  initRegions(state) {
    state.regions = JSON.parse(
      document.getElementById("regionsData").textContent
    );
  },
  initTeams(state) {
    state.teams = JSON.parse(document.getElementById("teamsData").textContent);
  },
  initUser(state) {
    state.user = JSON.parse(document.getElementById("userData").textContent);
  },
  setActiveTeamId(state, id) {
    state.activeTeamId = id;
  },
  setFilterTenantId(state, id) {
    state.filterTenantId = id;
  },
  setTeamInitialized(state) {
    state.teams.find(
      (team) => team.id === state.activeTeamId
    ).initialized = true;
  },
};

const actions = {
  async initStore({ commit }) {
    /* Initialise store from embedded Django template json */
    commit("initUser");
    commit("initRegions");
    commit("initTeams");
  },
  setActiveTeam({ commit }, team) {
    commit("setActiveTeamId", team.id);
    commit("setFilterTenantId", null);
  },
  setFilterTenant({ commit }, tenant) {
    /* allow null/undefined */
    commit("setFilterTenantId", tenant?.id);
  },
  async fetchTenantSpecificData(
    { commit, dispatch, getters, state },
    { tenant }
  ) {
    /* Fetch all tenant-specific data */
    try {
      await Promise.all([
        dispatch("flavors/getTeamFlavors", { tenant }),
        dispatch("images/getTeamImages", { tenant }),
        dispatch("instances/getTeamInstances", { tenant }),
        dispatch("keyPairs/getTeamKeyPairs", { tenant }),
        dispatch("volumeTypes/getTeamVolumeTypes", { tenant }),
        dispatch("volumes/getTeamVolumes", { tenant }),
      ]);
    } catch (err) {
      const msg = `Error fetching data from ${getters.getRegionNameForTenant(
        tenant
      )} tenant`;
      if (err.response && err.response.data.hasOwnProperty("detail")) {
        throw new Error(`${msg}: ${err.response.data.detail}`);
      } else {
        throw new Error(`${msg}: ${err.message}`);
      }
    }
  },
  async fetchTeamSpecificData({ dispatch }) {
    /* Fetch all team specific data (for the active team) */
    try {
      await dispatch("teamMembers/getTeamMembers");
    } catch (err) {
      const msg = `Error fetching team data for ${getters.team.name}`;
      if (err.response && err.response.data.hasOwnProperty("detail")) {
        throw new Error(`${msg}: ${err.response.data.detail}`);
      } else {
        throw new Error(`${msg}: ${err.message}`);
      }
    }
  },
  async fetchAll({ commit, dispatch, getters }) {
    if (!getters.team.initialized) {
      await dispatch("fetchTeamSpecificData"); // Will throw on err
      commit("setTeamInitialized");
    }
    const results = await Promise.allSettled([
      ...getters.tenants.map((tenant) =>
        dispatch("fetchTenantSpecificData", { tenant })
      ),
    ]);
    return results.map(({ status, value, reason }, index) => {
      return { status, value, reason, tenant: getters.tenants[index].id };
    });
  },
};

export default createStore({
  modules,
  state,
  getters,
  actions,
  mutations,
});
