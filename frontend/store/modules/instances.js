import { axios, apiRoutes } from "@/api";
import { updateTenantCollection } from "@/helpers";

const getDefaultState = () => {
  return {
    all: [],
    loading: false, // TODO: remove once refactored to component
    erroredOnGet: false,
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
  setLoading(state, loading) {
    state.loading = loading;
  },
  setErroredOnGet(state, erroredOnGet) {
    state.erroredOnGet = erroredOnGet;
  },
};

const getInstanceFormatter = (rootGetters) => {
  return (instance) => {
    const tenant = rootGetters.getTenantById(instance.tenant);
    const region = rootGetters.getRegionById(tenant.region);
    const flavor = rootGetters["flavors/getFlavorById"](instance.flavor);
    const timestamp = new Date(instance.created);
    const created = timestamp.toLocaleTimeString();

    return {
      region: region.name,
      name: instance.name,
      flavor: flavor?.name ?? "[legacy flavor]",
      status: instance.status,
      ip: instance.ip,
      created: created,
    };
  };
};

const getters = {
  allFormatted(state, _getters, _rootState, rootGetters) {
    return state.all.map(getInstanceFormatter(rootGetters));
  },
  notShelvedFormatted(_state, getters) {
    const shelvedStatus = ["SHELVED", "SHELVED_OFFLOADED"];
    return getters.allFormatted.filter(
      (instance) => shelvedStatus.indexOf(instance.status) == -1
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
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
