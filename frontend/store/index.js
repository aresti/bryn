import { createStore } from "vuex";

// Root getters, mutations, actions
import getters from "./getters";
import mutations from "./mutations";
import actions from "./actions";

// Modules
import flavors from "./modules/flavors";
import images from "./modules/images";
import instances from "./modules/instances";
import invitations from "./modules/invitations";
import keyPairs from "./modules/keyPairs";
import teamMembers from "./modules/teamMembers";
import volumes from "./modules/volumes";
import volumeTypes from "./modules/volumeTypes";

const state = {
  adminEmail: "Lisa.Marchioretto@quadram.ac.uk",
  activeTeamId: null,
  filterTenantId: null,
  regions: [],
  teams: [],
  user: null,
};

const modules = {
  flavors,
  images,
  instances,
  invitations,
  keyPairs,
  teamMembers,
  volumes,
  volumeTypes,
};

export default createStore({
  modules,
  state,
  getters,
  actions,
  mutations,
});
