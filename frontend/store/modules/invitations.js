import { axios, getAPIRoute } from "@/api";
import { collectionForTeamId } from "@/utils/store";

const state = () => {
  return {
    all: [],
  };
};

const mutations = {
  addInvitation(state, invitation) {
    state.all.unshift(invitation);
  },
  setInvitations(state, invitations) {
    state.all = invitations;
  },
  removeInvitationById(state, id) {
    state.all.splice(
      state.all.findIndex((obj) => obj.id === id),
      1
    );
  },
};

const getters = {
  allInvitations(state, _getters, rootState) {
    return state.all.filter(
      (invitation) => invitation.toTeam === rootState.activeTeamId
    );
  },
};

const actions = {
  async getInvitations({ commit, rootState }) {
    const url = getAPIRoute("invitations", rootState.activeTeamId);
    const response = await axios.get(url);
    const invitations = response.data;
    commit("setInvitations", invitations);
  },
  async createInvitation(
    { commit, rootGetters, rootState },
    { email, message }
  ) {
    const payload = {
      email,
      message,
      user: rootState.user.id,
      to_team: rootGetters.team.id,
    };
    const url = getAPIRoute("invitations", rootState.activeTeamId);
    const response = await axios.post(url, payload);
    const invitation = response.data;
    commit("addInvitation", invitation);
    return invitation;
  },
  async deleteInvitation({ commit }, invitation) {
    /* Delete an invitation */
    const url = getAPIRoute("invitations", invitation.toTeam) + invitation.uuid;
    await axios.delete(url);
    commit("removeInvitationById", invitation.uuid);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
