import { axios, apiRoutes } from "@/api";

const getDefaultState = () => {
  return {
    all: [],
    loading: false,
    erroredOnGet: false,
  };
};

// initial state
const state = getDefaultState();

const mutations = {
  resetState(state) {
    Object.assign(state, getDefaultState());
  },
  setInstances(state, instances) {
    state.all = instances;
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
  setErroredOnGet(state, erroredOnGet) {
    state.erroredOnGet = erroredOnGet;
  },
};

const getInstanceFormatter = (rootGetters) => {
  // Display formatter for instances
  return (instance) => {
    const tenant = rootGetters.getTenantById(instance.tenant);
    const region = rootGetters.getRegionById(tenant.id);
    const flavor = rootGetters["flavors/getFlavorById"](instance.flavor);
    const timestamp = new Date(instance.created);
    const created = timestamp.toUTCString();

    return {
      region: region.description,
      name: instance.name,
      flavor: flavor.name,
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
};

const actions = {
  async getTeamInstances({ rootState, commit }) {
    commit("setErroredOnGet", false);
    commit("setLoading", true);
    try {
      const response = await axios.get(apiRoutes.getInstances, {
        params: { team: rootState.activeTeam },
      });
      const instances = response.data;
      commit("setInstances", instances);
    } catch (err) {
      commit("setErroredOnGet", true);
      throw err;
    } finally {
      commit("setLoading", false);
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
