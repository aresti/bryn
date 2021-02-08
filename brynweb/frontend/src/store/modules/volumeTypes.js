import { axios, getAPIRoute } from "@/api";
import {
  updateTeamCollection,
  createFilterByTenantGetter,
} from "@/utils/store";

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
  async getTenantVolumeTypes({ commit, rootGetters }, tenant) {
    const team = rootGetters.team;
    const url = getAPIRoute("volumeTypes", team.id, tenant.id);
    const response = await axios.get(url);
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
