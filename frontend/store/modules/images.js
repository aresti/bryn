import { axios, apiRoutes } from "@/api";
import { updateTenantCollection } from "@/helpers";

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
  setImages(state, { images, tenant = {} }) {
    updateTenantCollection(state.all, images, { tenant });
  },
};

const getters = {
  getImageById(state) {
    return (id) => {
      return state.all.find((image) => image.id === id);
    };
  },
  getImagesForTenant(state) {
    return ({ id }) => {
      return state.all.filter((image) => image.tenant === id);
    };
  },
};

const actions = {
  async getTeamImages({ commit, rootState }, { tenant } = {}) {
    const response = await axios.get(apiRoutes.images, {
      params: { team: rootState.activeTeam },
    });
    const images = response.data;
    commit("setImages", { images, tenant });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
