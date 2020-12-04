import { axios, apiRoutes } from "@/api";
import { updateTenantCollection } from "@/helpers";

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
  setFlavors(state, { flavors, tenant = {} }) {
    updateTenantCollection(state.all, flavors, { tenant });
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
  async getTeamFlavors({ commit, rootState }, { tenant } = {}) {
    const response = await axios.get(apiRoutes.getFlavors, {
      params: { team: rootState.activeTeam },
    });
    const flavors = response.data;
    commit("setFlavors", { flavors, tenant });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
