import { createStore } from "vuex";
import { axios, apiRoutes } from "@/api";
import instances from "./modules/instances";
import flavors from "./modules/flavors";

export default createStore({
  state() {
    return {
      adminEmail: "Lisa.Marchioretto@quadram.ac.uk",
      initialized: false,
      activeTeam: null,
      user: null,
      regions: [],
      teams: [],
    };
  },
  modules: {
    instances,
    flavors,
  },
  getters: {
    userFullName(state) {
      return `${state.user.first_name} ${state.user.last_name}`;
    },
    team(state) {
      return state.teams.find((team) => team.id === state.activeTeam);
    },
    tenants(state, getters) {
      return state.activeTeam ? getters.team.tenants : [];
    },
    defaultTenant(state, getters) {
      return getters.tenants.find(
        (tenant) => tenant.region === getters.team.default_region
      );
    },
    getTenantById(state, getters) {
      return (id) => {
        return getters.tenants.find((tenant) => tenant.id === id);
      };
    },
    getRegionById(state) {
      return (id) => {
        return state.regions.find((region) => region.id === id);
      };
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
    initTeams(state, teams) {
      state.teams = JSON.parse(
        document.getElementById("teamsData").textContent
      );
    },
    initUser(state, user) {
      state.user = JSON.parse(document.getElementById("userData").textContent);
    },
    setActiveTeam(state, { id }) {
      state.activeTeam = id;
    },
    setFlavors(state, flavors) {
      state.flavors = flavors;
    },
    setImages(state, images) {
      state.images = images;
    },
  },
  actions: {
    initStore({ commit }) {
      commit("initUser");
      commit("initRegions");
      commit("initTeams");
      commit("setInitialized");
    },
    setActiveTeam({ commit }, team) {
      commit("setActiveTeam", team);
      commit("instances/resetState");
    },
    async getImages({ commit }) {
      const response = await axios.get(apiRoutes.getImages);
      const images = response.data;
      commit("setImages", images);
    },
    async getFlavors({ commit }) {
      const response = await axios.get(apiRoutes.getFlavors);
      const flavors = response.data;
      commit("setFlavors", flavors);
    },
  },
});
