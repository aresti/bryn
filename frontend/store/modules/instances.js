import { axios, apiRoutes } from "@/api";
import {
  pollingUtils,
  updateTeamCollection,
  collectionForTeamId,
  createFindByIdGetter,
  createFilterByTenantGetter,
} from "@/utils/store";

const SHELVED_STATUSES = ["SHELVED", "SHELVED_OFFLOADED"];

const getInstanceDetailUri = (instance) =>
  `${apiRoutes.instances}${instance.tenant}/${instance.id}`;

const state = () => {
  return {
    all: [],
    pollingSymbol: null, // Identifier for polling from setInterval()
    pollingTargets: [], // [{volumeId, ["targetStatus", "alternativeStatus"]}]
    loading: false,
  };
};

const mutations = {
  pollingAddTarget: pollingUtils.addTargetMutation,
  pollingRemoveTarget: pollingUtils.removeTargetMutation,
  pollingSetSymbol: pollingUtils.setSymbolMutation,
  pollingClearSymbol: pollingUtils.clearSymbolMutation,

  addInstance(state, instance) {
    state.all.unshift(instance);
  },
  setInstances(state, { instances, team, tenant }) {
    updateTeamCollection(state.all, instances, team, tenant);
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
  updateInstance(state, instance) {
    /* Update an existing instance, maintaining the ref */
    const target = state.all.find((target) => target.id === instance.id);
    if (target) {
      Object.assign(target, instance);
    }
  },
};

const getters = {
  getInstanceById(state) {
    return createFindByIdGetter(state.all);
  },
  getInstanceIsPolling(state) {
    return pollingUtils.createEntityIsPollingGetter(state);
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
  pollingAddTarget({ state, commit, dispatch }, { entity, status }) {
    pollingUtils.addTargetAction(
      { state, commit, dispatch },
      { entity, status, fetchActionName: "fetchInstance" }
    );
  },
  pollingFetchTargets: pollingUtils.fetchTargetsAction,
  pollingRemoveFulfilled: pollingUtils.removeFulfilledAction,

  async fetchInstance({ commit }, instance) {
    /* Fetch and update an individual instance */
    const uri = getInstanceDetailUri(instance);
    const response = await axios.get(uri);
    instance = response.data;
    commit("updateInstance", instance);
    return instance;
  },

  async createInstance(
    { commit, dispatch },
    { tenant, keypair, flavor, image, name }
  ) {
    const payload = { tenant, keypair, flavor, image, name };
    const response = await axios.post(apiRoutes.instances, payload);
    const instance = response.data;
    commit("addInstance", instance);
    dispatch("pollingAddTarget", {
      entity: instance,
      status: ["ACTIVE", "ERROR"],
    });
    return instance;
  },

  async targetInstanceStatus({ dispatch }, { instance, status }) {
    const payload = { status };
    const uri = getInstanceDetailUri(instance);
    await axios.patch(uri, payload);
    dispatch("pollingAddTarget", {
      entity: instance,
      status,
    });
  },

  async deleteInstance({ dispatch }, instance) {
    /* Delete an instance */
    const uri = getInstanceDetailUri(instance);
    await axios.delete(uri);
    dispatch("pollingAddTarget", {
      entity: instance,
    });
  },

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
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
