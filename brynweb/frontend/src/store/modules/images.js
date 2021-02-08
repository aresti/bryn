import { axios, getAPIRoute } from "@/api";
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
  setImages(state, { images, team, tenant }) {
    updateTeamCollection(state.all, images, team, tenant);
  },
};

const getters = {
  getImageById(state) {
    return createFindByIdGetter(state.all);
  },
  getImagesForTenant(state) {
    return createFilterByTenantGetter(state.all);
  },
};

const actions = {
  async getTenantImages({ commit, rootGetters }, tenant) {
    const team = rootGetters.team;
    const url = getAPIRoute("images", team.id, tenant.id);
    const response = await axios.get(url);
    const images = response.data;
    commit("setImages", { images, team, tenant });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
