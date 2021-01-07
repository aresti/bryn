import { axios, apiRoutes } from "@/api";
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
  async getInvitations({ commit }) {
    const response = await axios.get(apiRoutes.invitations);
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
    const uri = `${apiRoutes.invitations}`;
    const response = await axios.post(uri, payload);
    const invitation = response.data;
    commit("addInvitation", invitation);
    return invitation;
  },
  async deleteInvitation({ commit }, invitation) {
    /* Delete an invitation */
    const uri = `${apiRoutes.invitations}${invitation.uuid}`;
    await axios.delete(uri);
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
