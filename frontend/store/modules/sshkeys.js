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
  setSshKeys(state, { sshkeys, tenant = {} }) {
    updateTenantCollection(state.all, sshkeys, { tenant });
  },
};

const getters = {
  getSshKeyById(state) {
    return (id) => {
      return state.all.find((sshkey) => sshkey.id === id);
    };
  },
};

const actions = {
  async getTeamSshKeys({ commit, rootState }, { tenant } = {}) {
    const response = await axios.get(apiRoutes.getSshKeys, {
      params: { team: rootState.activeTeam },
    });
    const sshkeys = response.data;
    commit("setSshKeys", { sshkeys, tenant });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
