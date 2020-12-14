import { createStore } from "vuex";

import flavors from "./modules/flavors";
import images from "./modules/images";
import instances from "./modules/instances";
import keyPairs from "./modules/keypairs";
import teamMembers from "./modules/teamMembers";
import volumes from "./modules/volumes";

const state = {
  adminEmail: "Lisa.Marchioretto@quadram.ac.uk",
  activeTeam: null,
  filterTenant: null,
  loading: false,
  regions: [],
  teams: [],
  user: null,
};

const modules = {
  flavors,
  images,
  instances,
  keyPairs,
  volumes,
  teamMembers,
};

const getters = {
  userFullName(state) {
    return `${state.user.firstName} ${state.user.lastName}`;
  },
  team(state) {
    return state.teams.find((team) => team.id === state.activeTeam);
  },
  tenants(state, getters) {
    return state.activeTeam ? getters.team.tenants : [];
  },
  defaultTenant(_state, getters) {
    return getters.tenants.find(
      (tenant) => tenant.region === getters.team.defaultRegion
    );
  },
  getTenantById(_state, getters) {
    return (id) => {
      return getters.tenants.find((tenant) => tenant.id === id);
    };
  },
  getRegionById(state) {
    return (id) => {
      return state.regions.find((region) => region.id === id);
    };
  },
  getRegionNameForTenant(_state, getters) {
    return (tenant) => {
      const region = getters.getRegionById(tenant.region);
      return region?.description?.replace("University of ", "");
    };
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
  setActiveTeam(state, { id }) {
    state.activeTeam = id;
  },
  setFilterTenant(state, tenant) {
    state.filterTenant = tenant?.id;
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
};

const actions = {
  initStore({ commit }) {
    /* Initialise store from embedded Django template json */
    commit("initUser");
    commit("initRegions");
    commit("initTeams");
  },
  setActiveTeam({ commit }, team) {
    /* Set the activeTeam id and reset team-specific state */
    commit("setActiveTeam", team);
    commit("setFilterTenant", null);
    commit("instances/resetState");
    commit("images/resetState");
    commit("flavors/resetState");
    commit("keyPairs/resetState");
    commit("volumes/resetState");
    commit("teamMembers/resetState");
  },
  async getAllTenantData({ commit, dispatch, getters, state }, { tenant }) {
    /* Fetch all team data for a specific tenant */
    try {
      await Promise.all([
        dispatch("flavors/getTeamFlavors", { tenant }),
        dispatch("images/getTeamImages", { tenant }),
        dispatch("instances/getTeamInstances", { tenant }),
        dispatch("keyPairs/getTeamKeyPairs", { tenant }),
        dispatch("teamMembers/getTeamMembers"),
      ]);
      if (state.loading) {
        commit("setLoading", false);
      }
      await dispatch("volumes/getTeamVolumes", { tenant });
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
  async getAllTeamData({ commit, dispatch, getters }) {
    /* Fetch team data for all tenants */
    commit("setLoading", true);
    const results = await Promise.allSettled(
      getters.tenants.map((tenant) => dispatch("getAllTenantData", { tenant }))
    );
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
