import { axios, apiRoutes } from "@/api";
import {
  updateTeamCollection,
  createFindByIdGetter,
  createFilterByTenantGetter,
} from "@/utils/store";

const state = () => {
  return {
    all: [],
  };
};

const mutations = {
  setFlavors(state, { flavors, team, tenant }) {
    updateTeamCollection(state.all, flavors, team, tenant);
  },
};

const getters = {
  getFlavorById(state) {
    return createFindByIdGetter(state.all);
  },
  getFlavorsForTenant(state) {
    return createFilterByTenantGetter(state.all);
  },
};

const actions = {
  async getTeamFlavors({ commit, rootGetters }, { tenant } = {}) {
    const team = rootGetters.team;
    const response = await axios.get(apiRoutes.flavors, {
      params: { team: team.id, tenant: tenant?.id },
    });
    const flavors = response.data;
    commit("setFlavors", { flavors, team, tenant });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
