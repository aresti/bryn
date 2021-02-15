import { axios, getAPIRoute } from "@/api";
import {
  updateTeamCollection,
  createFindByIdGetter,
  createFilterByTenantGetter,
} from "@/utils/store";
import { SET_FLAVORS } from "./types";

const state = () => {
  return {
    all: [],
  };
};

const mutations = {
  [SET_FLAVORS](state, { flavors, team, tenant }) {
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
  async getTenantFlavors({ commit, rootGetters }, tenant) {
    const team = rootGetters.team;
    const url = getAPIRoute("flavors", team.id, tenant.id);
    const response = await axios.get(url);
    const flavors = response.data;
    commit(SET_FLAVORS, { flavors, team, tenant });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
