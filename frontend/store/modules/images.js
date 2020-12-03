import { axios, apiRoutes } from "@/api";

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
  setImages(state, images) {
    state.all = images;
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
  async getTeamImages({ commit, rootState }) {
    const response = await axios.get(apiRoutes.getImages, {
      params: { team: rootState.activeTeam },
    });
    const images = response.data;
    commit("setImages", images);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
