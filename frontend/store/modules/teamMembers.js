import { axios, apiRoutes } from "@/api";
import { collectionForTeamId } from "@/utils/store";

const state = () => {
  return {
    all: [],
  };
};

const mutations = {
  setTeamMembers(state, members) {
    state.all = members;
  },
};

const getters = {
  allTeamMembers(state, _getters, rootState) {
    return collectionForTeamId(state.all, rootState.activeTeamId);
  },
};

const actions = {
  async getTeamMembers({ commit }) {
    const response = await axios.get(apiRoutes.teamMembers);
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
