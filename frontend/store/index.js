import { createStore } from "vuex";

export default createStore({
  state() {
    return {
      user: null,
      teams: [],
      activeTeam: null,
      activeTenant: null,
    };
  },
  getters: {
    userFullName(state) {
      return `${state.user.first_name} ${state.user.last_name}`;
    },
    tenants(state) {
      if (state.activeTeam) {
        return state.activeTeam.tenants;
      } else {
        return [];
      }
    },
    defaultTenant(state, getters) {
      if (!getters.tenants.length) return null;
      if (!state.activeTeam.default_region) return self.tenants[0];
      for (let tenant of getters.tenants) {
        if (tenant.region.id === state.activeTeam.default_region) return tenant;
      }
    },
    activeTenantName(state) {
      return state.activeTenant.region.description;
    },
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setTeams(state, teams) {
      state.teams = teams;
    },
    setActiveTeam(state, team) {
      state.activeTeam = team;
    },
    setActiveTenant(state, tenant) {
      state.activeTenant = tenant;
    },
  },
  actions: {
    getUser({ dispatch, commit }) {
      const user = JSON.parse(document.getElementById("userData").textContent);
      commit("setUser", user);
      dispatch("getTeams");
    },
    getTeams({ dispatch, commit }) {
      const teams = JSON.parse(
        document.getElementById("teamsData").textContent
      );
      commit("setTeams", teams);
      dispatch("setActiveTeam", teams[0]);
    },
    setActiveTeam({ getters, commit }, team) {
      commit("setActiveTeam", team);
      commit("setActiveTenant", getters.defaultTenant);
    },
  },
});
