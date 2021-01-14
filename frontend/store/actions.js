import { axios, apiRoutes } from "@/api";

const actions = {
  async initStore({ commit, dispatch }) {
    /* Initialise store from embedded Django template json */
    commit("initUser");
    commit("initRegions");
    commit("initTeams");
    dispatch("keyPairs/getKeyPairs");
  },
  setActiveTeam({ commit }, team) {
    commit("setActiveTeamId", team.id);
    commit("setFilterTenantId", null);
  },
  setFilterTenant({ commit }, tenant) {
    /* allow null/undefined */
    commit("setFilterTenantId", tenant?.id);
  },

  async fetchTenantSpecificData({ _commit, dispatch, getters }, { tenant }) {
    /* Fetch all tenant-specific data */
    try {
      await Promise.all([
        dispatch("flavors/getTeamFlavors", { tenant }),
        dispatch("images/getTeamImages", { tenant }),
        dispatch("instances/getTeamInstances", { tenant }),
        dispatch("volumeTypes/getTeamVolumeTypes", { tenant }),
        dispatch("volumes/getTeamVolumes", { tenant }),
      ]);
    } catch (err) {
      const msg = `Error fetching data from ${getters.getRegionNameForTenant(
        tenant
      )} tenant`;
      if (err.response && err.response.data.hasOwnProperty("detail")) {
        throw new Error(`${msg}: ${err.response.data.detail}`);
      } else {
        throw new Error(`${msg}: ${err.message}`);
      }
    }
  },

  async fetchTeamSpecificData({ dispatch }) {
    /* Fetch all team specific data (for the active team) */
    try {
      await dispatch("teamMembers/getTeamMembers");
      await dispatch("invitations/getInvitations");
    } catch (err) {
      const msg = `Error fetching team data for ${getters.team.name}`;
      if (err.response && err.response.data.hasOwnProperty("detail")) {
        throw new Error(`${msg}: ${err.response.data.detail}`);
      } else {
        throw new Error(`${msg}: ${err.message}`);
      }
    }
  },

  async fetchUserSpecificData({ dispatch }) {
    /* Fetch all user specific data */
    try {
      await dispatch("keyPairs/getKeyPairs");
    } catch (err) {
      const msg = `Error fetching user data`;
      if (err.response && err.response.data.hasOwnProperty("detail")) {
        throw new Error(`${msg}: ${err.response.data.detail}`);
      } else {
        throw new Error(`${msg}: ${err.message}`);
      }
    }
  },

  async fetchAll({ commit, dispatch, getters }) {
    const tenants = getters.tenants; // remember, active team/tenants may have changed by the time function returns
    if (!getters.team.initialized) {
      await dispatch("fetchTeamSpecificData"); // Will throw on err
      commit("setTeamInitialized");
    }
    const results = await Promise.allSettled(
      tenants.map((tenant) => dispatch("fetchTenantSpecificData", { tenant }))
    );
    return results.map(({ status, value, reason }, index) => {
      return { status, value, reason, tenant: tenants[index].id };
    });
  },

  async updateTeam({ commit, getters }, teamData) {
    const uri = `${apiRoutes.team}${getters.team.id}`;
    const response = await axios.patch(uri, teamData);
    const team = response.data;
    commit("updateTeam", team);
  },

  async getUser({ commit }) {
    const uri = apiRoutes.userProfile;
    const response = await axios.get(uri);
    const user = response.data;
    commit("updateUser", user);
  },

  async updateUser({ commit }, userData) {
    const uri = apiRoutes.userProfile;
    const response = await axios.patch(uri, userData);
    const user = response.data;
    commit("updateUser", user);
  },
};

export default actions;
