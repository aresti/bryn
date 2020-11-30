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
  setSSHKeys(state, sshkeys) {
    state.all = sshkeys;
  },
};

const getters = {
  getSSHKeyById(state) {
    return (id) => {
      return state.all.find((sshkey) => sshkey.id === id);
    };
  },
};

const actions = {
  async getTeamSSHKeys({ commit, rootState }) {
    const response = await axios.get(apiRoutes.getSSHKeys, {
      params: { team: rootState.activeTeam },
    });
    const sshkeys = response.data;
    commit("setSSHKeys", sshkeys);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
