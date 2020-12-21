import { axios, apiRoutes } from "@/api";
import {
  updateTeamCollection,
  collectionForTeamId,
  createFilterByIdGetter,
  createFilterByTenantGetter,
} from "@/utils/store";

const SHELVED_STATUSES = ["SHELVED", "SHELVED_OFFLOADED"];

const state = () => {
  return {
    all: [],
    loading: false,
  };
};

const mutations = {
  setInstances(state, { instances, team, tenant }) {
    updateTeamCollection(state.all, instances, team, tenant);
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
};

const getters = {
  getInstanceById(state) {
    return createFilterByIdGetter(state.all);
  },
  getInstancesForTenant(state) {
    return createFilterByTenantGetter(state.all);
  },
  instancesForActiveTeam(state, _getters, rootState) {
    return collectionForTeamId(state.all, rootState.activeTeamId);
  },
  instancesForFilterTenant(_state, getters, rootState, rootGetters) {
    return rootState.filterTenantId
      ? getters.getInstancesForTenant(rootGetters.filterTenant)
      : getters.instancesForActiveTeam;
  },
  notShelvedForFilterTenant(_state, getters) {
    return getters.instancesForFilterTenant.filter(
      ({ status }) => SHELVED_STATUSES.indexOf(status) === -1
    );
  },
};

const actions = {
  async getTeamInstances({ rootGetters, commit }, { tenant } = {}) {
    commit("setLoading", true);
    const team = rootGetters.team;
    const response = await axios.get(apiRoutes.instances, {
      params: { team: team.id, tenant: tenant?.id },
    });
    const instances = response.data;
    commit("setInstances", { instances, team, tenant });
    commit("setLoading", false);
  },
  async createInstance({ commit }, data) {
    const response = await axios.post(apiRoutes.instances, data);
    console.log(response);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
