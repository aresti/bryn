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
  addKeyPair(state, keypair) {
    state.all.push(keypair);
  },
  removeKeyPairById(state, id) {
    state.all.splice(state.all.findIndex((obj) => obj.id === id));
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
    const response = await axios.get(apiRoutes.keyPairs, {
      params: { team: rootState.activeTeam },
    });
    const keypairs = response.data;
    commit("setKeyPairs", { keypairs, tenant });
  },
  async createKeyPair({ commit }, { tenant, name, publicKey }) {
    const payload = { tenant, name, publicKey };
    const response = await axios.post(apiRoutes.keyPairs, payload);
    const keypair = response.data;
    commit("addKeyPair", keypair);
    return keypair;
  },
  async deleteKeyPair({ commit }, { id, tenant }) {
    const uri = `${apiRoutes.keyPairs}${tenant}/${id}`;
    await axios.delete(uri);
    commit("removeKeyPairById", id);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
