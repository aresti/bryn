import { createStore } from "vuex";
import { axios } from "@/api";

export default createStore({
  state() {
    return {
      adminEmail: "Lisa.Marchioretto@quadram.ac.uk",
      initialized: false,
      activeTenant: undefined,
      user: undefined,
      regions: [],
      teams: [],
    };
  },
  getters: {
    userFullName(state) {
      return `${state.user.first_name} ${state.user.last_name}`;
    },
    team(state) {
      return state.teams.find((team) => team.id === state.activeTeam);
    },
    tenant(state, getters) {
      return getters.team.tenants.find(
        (tenant) => tenant.id === state.activeTenant
      );
    },
    tenants(state, getters) {
      return state.activeTeam ? getters.team.tenants : [];
    },
    tenantName(state, getters) {
      return "Tenant Name Stub";
      // return getters.tenant.region.description;
    },
    defaultTenant(state, getters) {
      return getters.tenants.find(
        (tenant) => tenant.region === getters.team.default_region
      );
    },
  },
  mutations: {
    setInitialized(state) {
      state.initialized = true;
    },
    initRegions(state) {
      state.regions = JSON.parse(
        document.getElementById("regionsData").textContent
      );
    },
    initUser(state, user) {
      state.user = JSON.parse(document.getElementById("userData").textContent);
    },
    initTeams(state, teams) {
      state.teams = JSON.parse(
        document.getElementById("teamsData").textContent
      );
    },
    setActiveTeam(state, { id }) {
      state.activeTeam = id;
    },
    setActiveTenant(state, { id }) {
      state.activeTenant = id;
    },
  },
  actions: {
    initStore({ commit }) {
      commit("initUser");
      commit("initRegions");
      commit("initTeams");
      commit("setInitialized");
    },
    setActiveTeam({ getters, commit }, team) {
      commit("setActiveTeam", team);
      if (getters.team.tenants.length) {
        commit("setActiveTenant", getters.defaultTenant);
      }
    },
    fetchImages({ getters, commit }) {},
  },
});
