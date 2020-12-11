import { axios, apiRoutes } from "@/api";
import { updateTenantCollection } from "@/helpers";

const getDefaultState = () => {
  return {
    all: [],
    loading: false,
  };
};

// initial state
const state = getDefaultState();

const mutations = {
  resetState(state) {
    Object.assign(state, getDefaultState());
  },
  setVolumes(state, { volumes, tenant = {} }) {
    updateTenantCollection(state.all, volumes, { tenant });
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
};

const getters = {
  volumesForFilterTenant(state, getters, rootState) {
    return rootState.filterTenant
      ? getters.getVolumesForTenant({ id: rootState.filterTenant })
      : state.all;
  },
  getKeyPairById(state) {
    return (id) => {
      return state.all.find((keypair) => keypair.id === id);
    };
  },
  getVolumesForTenant(state) {
    return ({ id }) => {
      return state.all.filter((keypair) => keypair.tenant === id);
    };
  },
};

const actions = {
  async getTeamVolumes({ commit, rootState }, { tenant } = {}) {
    commit("setLoading", true);
    const response = await axios.get(apiRoutes.getVolumes, {
      params: { team: rootState.activeTeam },
    });
    const volumes = response.data;
    commit("setVolumes", { volumes, tenant });
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
