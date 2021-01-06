import { axios, apiRoutes } from "@/api";

const actions = {
  async initStore({ commit }) {
    /* Initialise store from embedded Django template json */
    commit("initUser");
    commit("initRegions");
    commit("initTeams");
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
        dispatch("keyPairs/getTeamKeyPairs", { tenant }),
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
    } catch (err) {
      const msg = `Error fetching team data for ${getters.team.name}`;
      if (err.response && err.response.data.hasOwnProperty("detail")) {
        throw new Error(`${msg}: ${err.response.data.detail}`);
      } else {
        throw new Error(`${msg}: ${err.message}`);
      }
    }
  },

  async fetchAll({ commit, dispatch, getters }) {
    const tenants = getters.tenants; // store value, active team/tenants may have changed by the time function returns
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
};

export default actions;
