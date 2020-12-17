import { axios, apiRoutes } from "@/api";
import { updateTeamCollection, createFilterByTenantGetter } from "@/utils";

const state = () => {
  return {
    all: [],
  };
};

const mutations = {
  setVolumeTypes(state, { volumeTypes, team, tenant }) {
    updateTeamCollection(state.all, volumeTypes, team, tenant);
  },
};

const getters = {
  getVolumeTypesForTenant(state) {
    return createFilterByTenantGetter(state.all);
  },
};

const actions = {
  async getTeamVolumeTypes({ commit, rootGetters }, { tenant } = {}) {
    const team = rootGetters.team;
    const response = await axios.get(apiRoutes.volumeTypes, {
      params: { team: team.id, tenant: tenant?.id },
    });
    const volumeTypes = response.data;
    commit("setVolumeTypes", { volumeTypes, team, tenant });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
