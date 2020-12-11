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
  setTeamMembers(state, members) {
    state.all = members;
  },
};

const getters = {};

const actions = {
  async getTeamMembers({ commit, rootState }) {
    const response = await axios.get(apiRoutes.getTeamMembers, {
      params: { team: rootState.activeTeam },
    });
    const members = response.data;
    commit("setTeamMembers", members);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
