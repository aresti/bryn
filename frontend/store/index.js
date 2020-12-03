import { createStore } from "vuex";
import instances from "./modules/instances";
import flavors from "./modules/flavors";
import images from "./modules/images";
import sshkeys from "./modules/sshkeys";

const state = {
  adminEmail: "Lisa.Marchioretto@quadram.ac.uk",
  activeTeam: null,
  loading: false,
  regions: [],
  teams: [],
  user: null,
};

const modules = {
  flavors,
  images,
  instances,
  sshkeys,
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
};

const mutations = {
  initRegions(state) {
    state.regions = JSON.parse(
      document.getElementById("regionsData").textContent
    );
  },
  initTeams(state, teams) {
    state.teams = JSON.parse(document.getElementById("teamsData").textContent);
  },
  initUser(state, user) {
    state.user = JSON.parse(document.getElementById("userData").textContent);
  },
  setActiveTeam(state, { id }) {
    state.activeTeam = id;
  },
  setLoading(state, loading) {
    state.loading = !state.loading;
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
    commit("instances/resetState");
    commit("images/resetState");
    commit("flavors/resetState");
    commit("sshkeys/resetState");
  },
  async getAllTeamData({ dispatch, commit }) {
    /* Fetch all team data */
    commit("setLoading", true);
    try {
      await Promise.all([
        dispatch("flavors/getTeamFlavors"),
        dispatch("images/getTeamImages"),
        dispatch("instances/getTeamInstances"),
        dispatch("sshkeys/getTeamSSHKeys"),
      ]);
    } catch (err) {
      if (err.response && err.response.data.hasOwnProperty("detail")) {
        throw new Error(
          `Error fetching team data: ${err.response.data.detail}`
        );
      } else {
        throw new Error(`Error fetching team data: ${err.message}`);
      }
    } finally {
      commit("setLoading", false);
    }
  },
};

export default createStore({
  modules,
  state,
  getters,
  actions,
  mutations,
});
