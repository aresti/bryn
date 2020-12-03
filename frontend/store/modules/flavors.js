import { axios, apiRoutes } from "@/api";

const getDefaultState = () => {
  return {
    all: [],
  };
};

// initial state
const state = getDefaultState();

const mutations = {
  resetState(state) {
    Object.assign(state, getDefaultState());
  },
  setFlavors(state, flavors) {
    state.all = flavors;
  },
};

const getters = {
  getFlavorById(state) {
    return (id) => {
      return state.all.find((flavor) => flavor.id === id);
    };
  },
  getFlavorsForTenant(state) {
    return ({ id }) => {
      return state.all.filter((flavor) => flavor.tenant === id);
    };
  },
};

const actions = {
  async getTeamFlavors({ commit, rootState }) {
    const response = await axios.get(apiRoutes.getFlavors, {
      params: { team: rootState.activeTeam },
    });
    const flavors = response.data;
    commit("setFlavors", flavors);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
