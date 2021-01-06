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
  async getTeamMembers({ commit }) {
    const response = await axios.get(apiRoutes.teamMembers);
    const members = response.data;
    commit("setTeamMembers", members);
  },
  async deleteTeamMember({ commit }, teamMember) {
    /* Delete a team member */
    const uri = `${apiRoutes.teamMembers}${teamMember.id}`;
    await axios.delete(uri);
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
