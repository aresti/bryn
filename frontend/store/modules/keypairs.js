import { axios, apiRoutes } from "@/api";
import {
  updateTeamCollection,
  collectionForTeamId,
  createFilterByIdGetter,
  createFilterByTenantGetter,
} from "@/utils/store";

const state = () => {
  return {
    all: [],
  };
};

const mutations = {
  setKeyPairs(state, { keyPairs, team, tenant }) {
    updateTeamCollection(state.all, keyPairs, team, tenant);
  },
  addKeyPair(state, keyPair) {
    state.all.unshift(keyPair);
  },
  removeKeyPairById(state, id) {
    state.all.splice(
      state.all.findIndex((obj) => obj.id === id),
      1
    );
  },
};

const getters = {
  getKeyPairById(state) {
    return createFilterByIdGetter(state.all);
  },
  getKeyPairsForTenant(state) {
    return createFilterByTenantGetter(state.all);
  },
  keyPairsForActiveTeam(state, _getters, rootState) {
    return collectionForTeamId(state.all, rootState.activeTeamId);
  },
  keyPairsForFilterTenant(_state, getters, rootState, rootGetters) {
    return rootState.filterTenantId
      ? getters.getKeyPairsForTenant(rootGetters.filterTenant)
      : getters.keyPairsForActiveTeam;
  },
};

const actions = {
  async getTeamKeyPairs({ commit, rootGetters }, { tenant } = {}) {
    const team = rootGetters.team;
    const response = await axios.get(apiRoutes.keyPairs, {
      params: { team: team.id, tenant: tenant?.id },
    });
    const keyPairs = response.data;
    commit("setKeyPairs", { keyPairs, team, tenant });
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
