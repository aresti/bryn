import { axios, getAPIRoute } from "@/api";

const actions = {
  async initStore({ commit, dispatch }) {
    /* Initialise store from embedded Django template json */
    commit("initUser");
    commit("initRegions");
    commit("initTeams");
    await dispatch("keyPairs/getKeyPairs");
  },
  setActiveTeam({ commit }, team) {
    commit("setActiveTeamId", team.id);
    commit("setFilterTenantId", null);
  },
  setFilterTenant({ commit }, tenant) {
    /* allow null/undefined */
    commit("setFilterTenantId", tenant?.id);
  },

  async fetchTenantSpecificData({ _commit, dispatch, getters }, tenant) {
    /* Fetch all tenant-specific data */
    try {
      await Promise.all([
        dispatch("flavors/getTenantFlavors", tenant),
        dispatch("images/getTenantImages", tenant),
        dispatch("instances/getTenantInstances", tenant),
        dispatch("volumeTypes/getTenantVolumeTypes", tenant),
        dispatch("volumes/getTenantVolumes", tenant),
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

  async fetchTeamSpecificData({ commit, dispatch, getters }) {
    /* Fetch all team specific data (for the active team) */
    if (!getters.team.initialized) {
      try {
        await dispatch("teamMembers/getTeamMembers");
        await dispatch("invitations/getInvitations");
        commit("setTeamInitialized");
      } catch (err) {
        const msg = `Error fetching team data for ${getters.team.name}`;
        if (err.response && err.response.data.hasOwnProperty("detail")) {
          throw new Error(`${msg}: ${err.response.data.detail}`);
        } else {
          throw new Error(`${msg}: ${err.message}`);
        }
      }
    }
  },

  async fetchAllTenantData({ dispatch, getters }) {
    const tenants = getters.tenants; // remember, active team/tenants may have changed by the time function returns

    if (!tenants.length) {
      throw new Error(`The current team has no tenants.`);
    }

    const results = await Promise.allSettled(
      tenants.map((tenant) => dispatch("fetchTenantSpecificData", tenant))
    );
    return results.map(({ status, value, reason }, index) => {
      return { status, value, reason, tenant: tenants[index].id };
    });
  },

  async updateTeam({ commit, getters }, teamData) {
    const url = `${getAPIRoute("teams")}${getters.team.id}`;
    const response = await axios.patch(url, teamData);
    const team = response.data;
    commit("updateTeam", team);
  },

  async getUser({ commit }) {
    const url = getAPIRoute("userProfile");
    const response = await axios.get(url);
    const user = response.data;
    commit("updateUser", user);
  },

  async updateUser({ commit }, userData) {
    const url = getAPIRoute("userProfile");
    const response = await axios.patch(url, userData);
    const user = response.data;
    commit("updateUser", user);
  },
};

export default actions;
