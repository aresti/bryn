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
  setKeyPairs(state, { keypairs, tenant = {} }) {
    updateTenantCollection(state.all, keypairs, { tenant });
  },
};

const getters = {
  keyPairsForFilterTenant(state, _getters, rootState) {
    if (rootState.filterTenant == null) {
      return state.all;
    }
    return state.all.filter(
      (instance) => instance.tenant === rootState.filterTenant
    );
  },
  getKeyPairById(state) {
    return (id) => {
      return state.all.find((keypair) => keypair.id === id);
    };
  },
  getKeyPairsForTenant(state) {
    return ({ id }) => {
      return state.all.filter((keypair) => keypair.tenant === id);
    };
  },
};

const actions = {
  async getTeamKeyPairs({ commit, rootState }, { tenant } = {}) {
    const response = await axios.get(apiRoutes.getKeyPairs, {
      params: { team: rootState.activeTeam },
    });
    const keypairs = response.data;
    commit("setKeyPairs", { keypairs, tenant });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
