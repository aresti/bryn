import { axios, apiRoutes } from "@/api";
import {
  updateTeamCollection,
  createFilterByIdGetter,
  createFilterByTenantGetter,
} from "@/utils";

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
    return createFilterByIdGetter(state.all);
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
