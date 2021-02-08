import { axios, getAPIRoute } from "@/api";
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
  getKeyPairIsDefault(_state, _getters, rootState) {
    return ({ id }) => id === rootState.user.profile.defaultKeypair;
  },
  defaultKeyPair(_state, getters, rootState) {
    const defaultKeyPairId = rootState.user.profile.defaultKeypair;
    if (defaultKeyPairId == null) {
      return null;
    } else {
      return getters.getKeyPairById(defaultKeyPairId);
    }
  },
};

const actions = {
  async getKeyPairs({ commit }) {
    const url = getAPIRoute("keyPairs");
    const response = await axios.get(url);
    const keyPairs = response.data;
    commit("setKeyPairs", keyPairs);
  },
  async createKeyPair({ commit, dispatch, state }, { name, publicKey }) {
    const payload = { name, publicKey };
    const url = getAPIRoute("keyPairs");
    const response = await axios.post(url, payload);
    const keypair = response.data;
    commit("addKeyPair", keypair);
    if (state.all.length == 1) {
      // First is auto-set to default, update user data on frontend
      dispatch("getUser", null, { root: true });
    }
    return keypair;
  },
  async deleteKeyPair({ commit, dispatch, getters }, keyPair) {
    const url = `${getAPIRoute("keyPairs")}${keyPair.id}`;
    const wasDefault = getters.getKeyPairIsDefault(keyPair);
    await axios.delete(url);
    commit("removeKeyPairById", keyPair.id);
    if (wasDefault) {
      // User default will have changed
      dispatch("getUser", null, { root: true });
    }
  },
  async setDefaultKeyPair({ dispatch }, { id }) {
    const userData = { profile: { default_keypair: id } };
    await dispatch("updateUser", userData, { root: true });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
