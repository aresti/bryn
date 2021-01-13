import { axios, apiRoutes } from "@/api";
import { createFindByIdGetter } from "@/utils/store";

const state = () => {
  return {
    all: [],
  };
};

const mutations = {
  setKeyPairs(state, keyPairs) {
    state.all = keyPairs;
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
    return createFindByIdGetter(state.all);
  },
};

const actions = {
  async getKeyPairs({ commit }) {
    const response = await axios.get(apiRoutes.keyPairs);
    const keyPairs = response.data;
    commit("setKeyPairs", keyPairs);
  },
  async createKeyPair({ commit }, { name, publicKey }) {
    const payload = { name, publicKey };
    const response = await axios.post(apiRoutes.keyPairs, payload);
    const keypair = response.data;
    commit("addKeyPair", keypair);
    return keypair;
  },
  async deleteKeyPair({ commit }, { id }) {
    const uri = `${apiRoutes.keyPairs}${id}`;
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
