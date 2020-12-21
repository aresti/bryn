import { axios, apiRoutes } from "@/api";
import {
  updateTeamCollection,
  collectionForTeamId,
  createFilterByIdGetter,
  createFilterByTenantGetter,
} from "@/utils";

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
  addPollingTarget(state, { volume, status = null }) {
    /*
     * Add a polling 'target' object
     * Target object format:
     *  - {volumeId, ["targetStatus", "alternativeStatus"]}
     *  - OR {volumeId, "singleStringStatus"}
     * Will be removed once volume status has reached one of the target states
     * 404 (following deletion): remove polling target and volume.
     */
    const existingTarget = state.pollingTargets.find(
      (target) => target.volumeId === volume.id
    );

    if (existingTarget) {
      /* Don't add duplicate targets; update status only */
      existingTarget.status = status;
    } else {
      state.pollingTargets.push({ volumeId: volume.id, status });
    }
  },
  removePollingTargetByVolumeId(state, volumeId) {
    state.pollingTargets.splice(
      state.pollingTargets.findIndex((obj) => obj.volumeId === volumeId),
      1
    );
  },
  setPollingSymbol(state, pollingSymbol) {
    state.pollingSymbol = pollingSymbol;
  },
  removePollingSymbol(state) {
    state.pollingSymbol = null;
  },
  updateVolume(state, volume) {
    /* Update an existing volume, maintaining the ref */
    const target = state.all.find((target) => target.id === volume.id);
    if (target) {
      Object.assign(target, volume);
    }
  },
  removeVolumeById(state, id) {
    state.all.splice(
      state.all.findIndex((obj) => obj.id === id),
      1
    );
  },
};

const getters = {
  getVolumeById(state) {
    return createFilterByIdGetter(state.all);
  },
  getVolumeIsPolling(state) {
    /* Return a getter to check whether a volume has a polling target */
    return (volume) => {
      return state.pollingTargets.some(
        (target) => target.volumeId === volume.id
      );
    };
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
  async createVolume({ commit, dispatch }, { tenant, volumeType, size, name }) {
    const payload = { tenant, volumeType, size, name };
    const response = await axios.post(apiRoutes.volumes, payload);
    const volume = response.data;
    commit("addVolume", volume);
    dispatch("addPollingTarget", {
      volume,
      status: ["available", "in-use", "error"],
    });
    return volume;
  },
  addPollingTarget({ state, commit, dispatch }, { volume, status }) {
    commit("addPollingTarget", { volume, status });
    dispatch("fetchPollingTargets"); // First/immediate update
    if (!state.pollingSymbol) {
      /* Start polling */
      const pollingSymbol = setInterval(() => {
        console.log("polling");
        dispatch("fetchPollingTargets");
      }, 5000);
      commit("setPollingSymbol", pollingSymbol);
    }
  },
  removeFulfilledPollingTargets({ commit, getters, state }) {
    /* Remove any polling targets, where the volume has reached target status */
    for (let i = state.pollingTargets.length - 1; i >= 0; i--) {
      const target = state.pollingTargets[i];
      const volume = getters.getVolumeById(target.volumeId);
      const status =
        typeof target.status == "string" ? [target.status] : target.status;

      if (status == null) {
        // resolves by 404, skip this test
        continue;
      }

      if (status.includes(volume.status)) {
        commit("removePollingTargetByVolumeId", volume.id);
      }
    }
    if (!state.pollingTargets.length) {
      /* Stop polling */
      clearInterval(state.pollingSymbol);
      commit("removePollingSymbol");
    }
  },
  async fetchPollingTargets({ commit, dispatch, state, getters }) {
    /* Fetch & update all polling targets */
    const results = await Promise.allSettled(
      state.pollingTargets.map((target) => {
        const volume = getters.getVolumeById(target.volumeId);
        return dispatch("fetchVolume", { volume });
      })
    );

    /* Check for 404 (deleted): remove polling targets and volumes*/
    results.forEach((result, index) => {
      if (
        result.status == "rejected" &&
        result.reason.response?.status === 404
      ) {
        const volumeId = state.pollingTargets[index].volumeId;
        commit("removePollingTargetByVolumeId", volumeId);
        commit("removeVolumeById", volumeId);
      }
    });

    /* Remove fulfilled polling targets */
    dispatch("removeFulfilledPollingTargets");
  },
  async fetchVolume({ commit }, { volume }) {
    /* Fetch and update an individual volume */
    const uri = getVolumeDetailUri(volume);
    const response = await axios.get(uri);
    volume = response.data;
    commit("updateVolume", volume);
    return volume;
  },
  async deleteVolume({ dispatch }, volume) {
    /* Delete a volume */
    const uri = getVolumeDetailUri(volume);
    await axios.delete(uri);
    dispatch("addPollingTarget", {
      volume,
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
  async attachVolume({ dispatch }, { volume, server }) {
    const payload = { attachments: [{ serverId: server.id }] };
    const uri = getVolumeDetailUri(volume);
    await axios.patch(uri, payload);
    dispatch("addPollingTarget", {
      volume,
      status: "in-use",
    });
  },
  async detachVolume({ dispatch }, volume) {
    const payload = { attachments: [] }; // Empty array
    const uri = getVolumeDetailUri(volume);
    await axios.patch(uri, payload);
    dispatch("addPollingTarget", {
      volume,
      status: "available",
    });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
