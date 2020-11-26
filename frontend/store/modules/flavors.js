import { axios, apiRoutes } from "@/api";

const getDefaultState = () => {
  return {
    all: [],
    loading: false,
    erroredOnGet: false,
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
  setLoading(state, loading) {
    state.loading = loading;
  },
  setErroredOnGet(state, erroredOnGet) {
    state.erroredOnGet = erroredOnGet;
  },
};

const getters = {
  getFlavorById(state) {
    return (id) => {
      return state.all.find((flavor) => flavor.id === id);
    };
  },
};

const actions = {
  async getTeamFlavors({ commit, rootState }) {
    commit("setErroredOnGet", false);
    commit("setLoading", true);
    try {
      const response = await axios.get(apiRoutes.getFlavors, {
        params: { team: rootState.activeTeam },
      });
      const flavors = response.data;
      commit("setFlavors", flavors);
    } catch (err) {
      commit("setErroredOnGet", true);
      throw err;
    } finally {
      commit("setLoading", false);
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
