import { createStore } from "vuex";

export default createStore({
  state() {
    return {
      activeTeam: undefined,
      activeTenant: undefined,
      user: undefined,
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
      return getters.tenant.region.description;
    },
    defaultTenant(state, getters) {
      return getters.tenants.find(
        (tenant) => tenant.region.id === getters.team.default_region
      );
    },
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setTeams(state, teams) {
      state.teams = teams;
    },
    setActiveTeam(state, { id }) {
      state.activeTeam = id;
    },
    setActiveTenant(state, { id }) {
      state.activeTenant = id;
    },
  },
  actions: {
    initStore({ dispatch, commit }) {
      const user = JSON.parse(document.getElementById("userData").textContent);
      const teams = JSON.parse(
        document.getElementById("teamsData").textContent
      );
      commit("setUser", user);
      if (teams.length) {
        commit("setTeams", teams);
        dispatch("setActiveTeam", teams[0]);
      }
    },
    setActiveTeam({ getters, commit }, team) {
      commit("setActiveTeam", team);
      commit("setActiveTenant", getters.defaultTenant);
    },
  },
});
