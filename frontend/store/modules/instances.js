import { axios, apiRoutes } from "@/api";
import { updateTenantCollection } from "@/helpers";

const SHELVED_STATUSES = ["SHELVED", "SHELVED_OFFLOADED"];

const getDefaultState = () => {
  return {
    all: [],
  };
};

// initial state
const state = getDefaultState();

const mutations = {
  resetState(state) {
    Object.assign(state, getDefaultState());
  },
  setInstances(state, { instances, tenant = {} }) {
    updateTenantCollection(state.all, instances, { tenant });
  },
};

const getters = {
  getInstancesForTenant(state) {
    return ({ id }) => {
      return state.all.filter((instance) => instance.tenant === id);
    };
  },
  instancesForFilterTenant(state, _getters, rootState) {
    if (rootState.filterTenant == null) {
      return state.all;
    }
    return state.all.filter(
      (instance) => instance.tenant === rootState.filterTenant
    );
  },
  notShelvedForFilterTenant(_state, getters) {
    return getters.instancesForFilterTenant.filter(
      ({ status }) => SHELVED_STATUSES.indexOf(status) === -1
    );
  },
};

const actions = {
  async getTeamInstances({ rootState, commit }, { tenant } = {}) {
    // If no tenant specified, fetch all for active team
    const params =
      tenant == null ? { team: rootState.activeTeam } : { tenant: tenant.id };
    const response = await axios.get(apiRoutes.getInstances, {
      params: params,
    });
    const instances = response.data;
    commit("setInstances", { instances, tenant });
  },
  async createInstance({ commit }, data) {
    const response = await axios.post(apiRoutes.postInstance, data);
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
