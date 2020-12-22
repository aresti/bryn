import { axios, apiRoutes } from "@/api";
import {
  updateTeamCollection,
  collectionForTeamId,
  pollingUtils,
  createFilterByIdGetter,
  createFilterByTenantGetter,
} from "@/utils/store";

const getVolumeDetailUri = (volume) =>
  `${apiRoutes.volumes}${volume.tenant}/${volume.id}`;

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

  addVolume(state, volume) {
    state.all.unshift(volume);
  },
  setVolumes(state, { volumes, team, tenant }) {
    /* Update all volumes for a team (fetch [and replace]) */
    updateTeamCollection(state.all, volumes, team, tenant);
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
  updateVolume(state, volume) {
    /* Update an existing volume, maintaining the ref */
    const target = state.all.find((target) => target.id === volume.id);
    if (target) {
      Object.assign(target, volume);
    }
  },
};

const getters = {
  getVolumeById(state) {
    return createFilterByIdGetter(state.all);
  },
  getVolumeIsPolling(state) {
    return pollingUtils.createEntityIsPollingGetter(state);
  },
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
  pollingAddTarget({ state, commit, dispatch }, { entity, status }) {
    pollingUtils.addTargetAction(
      { state, commit, dispatch },
      { entity, status, fetchActionName: "fetchVolume" }
    );
  },
  pollingFetchTargets: pollingUtils.fetchTargetsAction,
  pollingRemoveFulfilled: pollingUtils.removeFulfilledAction,

  async fetchVolume({ commit }, volume) {
    /* Fetch and update an individual volume */
    const uri = getVolumeDetailUri(volume);
    const response = await axios.get(uri);
    volume = response.data;
    commit("updateVolume", volume);
    return volume;
  },

  async createVolume({ commit, dispatch }, { tenant, volumeType, size, name }) {
    const payload = { tenant, volumeType, size, name };
    const response = await axios.post(apiRoutes.volumes, payload);
    const volume = response.data;
    commit("addVolume", volume);
    dispatch("pollingAddTarget", {
      entity: volume,
      status: ["available", "in-use", "error"],
    });
    return volume;
  },

  async deleteVolume({ dispatch }, volume) {
    /* Delete a volume */
    const uri = getVolumeDetailUri(volume);
    await axios.delete(uri);
    dispatch("pollingAddTarget", {
      entity: volume,
    });
  },

  async attachVolume({ dispatch }, { volume, server }) {
    const payload = { attachments: [{ serverId: server.id }] };
    const uri = getVolumeDetailUri(volume);
    await axios.patch(uri, payload);
    dispatch("pollingAddTarget", {
      entity: volume,
      status: "in-use",
    });
  },

  async detachVolume({ dispatch }, volume) {
    const payload = { attachments: [] }; // Empty array
    const uri = getVolumeDetailUri(volume);
    await axios.patch(uri, payload);
    dispatch("pollingAddTarget", {
      entity: volume,
      status: "available",
    });
  },

  async getTeamVolumes({ commit, rootGetters }, { tenant } = {}) {
    /* Fetch [and replace] all volumes for the active team */
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
