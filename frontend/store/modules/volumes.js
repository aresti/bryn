import { axios, apiRoutes } from "@/api";
import {
  updateTeamCollection,
  collectionForTeamId,
  createFilterByTenantGetter,
} from "@/utils";

const state = () => {
  return {
    all: [],
    loading: false,
  };
};

const mutations = {
  setVolumes(state, { volumes, team, tenant }) {
    updateTeamCollection(state.all, volumes, team, tenant);
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
};

const getters = {
  getVolumesForTenant(state) {
    return createFilterByTenantGetter(state.all);
  },
  volumesForActiveTeam(state, _getters, rootState) {
    return collectionForTeamId(state.all, rootState.activeTeamId);
  },
  volumesForFilterTenant(_state, getters, rootState, rootGetters) {
    return rootState.filterTenantId
      ? getters.getVolumesForTenant(rootGetters.filterTenant)
      : getters.volumesForActiveTeam;
  },
};

const actions = {
  async getTeamVolumes({ commit, rootGetters }, { tenant } = {}) {
    commit("setLoading", true);
    const team = rootGetters.team;
    const response = await axios.get(apiRoutes.volumes, {
      params: { team: team.id, tenant: tenant?.id },
    });
    const volumes = response.data;
    commit("setVolumes", { volumes, team, tenant });
    commit("setLoading", false);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
