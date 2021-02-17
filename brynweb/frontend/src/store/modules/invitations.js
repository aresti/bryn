import { axios, getAPIRoute } from "@/api";
import {
  CREATE_INVITATION,
  DELETE_INVITATION,
  FETCH_INVITATIONS,
} from "@/store/action-types";
import { ALL_INVITATIONS, TEAM } from "@/store/getter-types";
import {
  ADD_INVITATION,
  REMOVE_INVITATION_BY_ID,
  SET_INVITATIONS,
} from "@/store/mutation-types";

const state = () => {
  return {
    all: [],
  };
};

const mutations = {
  [ADD_INVITATION](state, invitation) {
    state.all.unshift(invitation);
  },

  [SET_INVITATIONS](state, invitations) {
    state.all = invitations;
  },

  [REMOVE_INVITATION_BY_ID](state, uuid) {
    state.all.splice(
      state.all.findIndex((obj) => obj.uuid === uuid),
      1
    );
  },
};

const getters = {
  [ALL_INVITATIONS](state, _getters, rootState) {
    return state.all.filter(
      (invitation) => invitation.toTeam === rootState.activeTeamId
    );
  },
};

const actions = {
  async [FETCH_INVITATIONS]({ commit, rootState }) {
    const url = getAPIRoute("invitations", rootState.activeTeamId);
    const response = await axios.get(url);
    const invitations = response.data;
    commit(SET_INVITATIONS, invitations);
  },

  async [CREATE_INVITATION](
    { commit, rootGetters, rootState },
    { email, message }
  ) {
    const payload = {
      email,
      message,
      user: rootState.user.id,
      to_team: rootGetters[TEAM].id,
    };
    const url = getAPIRoute("invitations", rootState.activeTeamId);
    const response = await axios.post(url, payload);
    const invitation = response.data;
    commit(ADD_INVITATION, invitation);
    return invitation;
  },

  async [DELETE_INVITATION]({ commit, rootState }, invitation) {
    /* Delete an invitation */
    const url =
      getAPIRoute("invitations", rootState.activeTeamId) + invitation.uuid;
    await axios.delete(url);
    commit(REMOVE_INVITATION_BY_ID, invitation.uuid);
  },
};

export default {
  namespaced: false,
  state,
  getters,
  actions,
  mutations,
};
