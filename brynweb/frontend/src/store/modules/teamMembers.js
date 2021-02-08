import { axios, getAPIRoute } from "@/api";
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
  removeTeamMemberById(state, id) {
    state.all.splice(
      state.all.findIndex((obj) => obj.id === id),
      1
    );
  },
};

const getters = {
  allTeamMembers(state, _getters, rootState) {
    return collectionForTeamId(state.all, rootState.activeTeamId);
  },
  adminTeamMembers(_state, getters) {
    return getters.allTeamMembers.filter((member) => member.isAdmin);
  },
};

const actions = {
  async getTeamMembers({ commit, rootState }) {
    const url = getAPIRoute("teamMembers", rootState.activeTeamId);
    const response = await axios.get(url);
    const members = response.data;
    commit("setTeamMembers", members);
  },
  async deleteTeamMember({ commit }, teamMember) {
    /* Delete a team member */
    const url = `${getAPIRoute("teamMembers", teamMember.team)}${
      teamMember.id
    }`;
    await axios.delete(url);
    commit("removeTeamMemberById", teamMember.id);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
