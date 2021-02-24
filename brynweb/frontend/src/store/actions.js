import { axios, getAPIRoute } from "@/api";

import {
  FETCH_ALL_TENANT_DATA,
  FETCH_ANNOUNCEMENTS,
  FETCH_HYPERVISOR_STATS,
  FETCH_INVITATIONS,
  FETCH_KEY_PAIRS,
  FETCH_TENANT_FLAVORS,
  FETCH_TENANT_IMAGES,
  FETCH_TEAM_MEMBERS,
  FETCH_TEAM_SPECIFIC_DATA,
  FETCH_TENANT_INSTANCES,
  FETCH_TENANT_SPECIFIC_DATA,
  FETCH_TENANT_VOLUME_TYPES,
  FETCH_TENANT_VOLUMES,
  FETCH_USER,
  INIT_STORE,
  SET_ACTIVE_TEAM,
  SET_FILTER_TENANT,
  UPDATE_TEAM,
  UPDATE_USER,
} from "./action-types";
import { GET_REGION_NAME_FOR_TENANT, TEAM, TENANTS } from "./getter-types";
import {
  INIT_REGIONS,
  INIT_TEAMS,
  INIT_USER,
  SET_ACTIVE_TEAM_ID,
  SET_HYPERVISOR_STATS,
  SET_FILTER_TENANT_ID,
  SET_TEAM_INITIALIZED,
  MODIFY_TEAM,
  SET_USER,
} from "./mutation-types";

const actions = {
  async [INIT_STORE]({ commit, dispatch }) {
    /* Initialise store from embedded Django template json */
    commit(INIT_USER);
    commit(INIT_REGIONS);
    commit(INIT_TEAMS);
    await Promise.all([
      dispatch(FETCH_KEY_PAIRS),
      dispatch(FETCH_HYPERVISOR_STATS),
      dispatch(FETCH_ANNOUNCEMENTS),
    ]);
  },

  [SET_ACTIVE_TEAM]({ commit }, team) {
    commit(SET_ACTIVE_TEAM_ID, team.id);
    commit(SET_FILTER_TENANT_ID, null);
  },

  [SET_FILTER_TENANT]({ commit }, tenant) {
    /* allow null/undefined */
    commit(SET_FILTER_TENANT_ID, tenant?.id);
  },

  async [FETCH_HYPERVISOR_STATS]({ commit }) {
    const url = getAPIRoute("hypervisorStats");
    const response = await axios.get(url);
    const hypervisorStats = response.data;
    commit(SET_HYPERVISOR_STATS, hypervisorStats);
  },

  async [FETCH_TENANT_SPECIFIC_DATA]({ dispatch, getters }, tenant) {
    /* Fetch all tenant-specific data */
    try {
      await Promise.all([
        dispatch(FETCH_TENANT_FLAVORS, tenant),
        dispatch(FETCH_TENANT_IMAGES, tenant),
        dispatch(FETCH_TENANT_INSTANCES, tenant),
        dispatch(FETCH_TENANT_VOLUME_TYPES, tenant),
        dispatch(FETCH_TENANT_VOLUMES, tenant),
      ]);
    } catch (err) {
      const msg = `Error fetching data from ${getters[
        GET_REGION_NAME_FOR_TENANT
      ](tenant)} tenant`;
      if (
        err.response &&
        Object.prototype.hasOwnProperty.call(err.response.data, "detail")
      ) {
        throw new Error(`${msg}: ${err.response.data.detail}`);
      } else {
        throw new Error(`${msg}: ${err.message}`);
      }
    }
  },

  async [FETCH_TEAM_SPECIFIC_DATA]({ commit, dispatch, getters }) {
    /* Fetch all team specific data (for the active team) */
    if (!getters[TEAM].initialized) {
      try {
        await dispatch(FETCH_TEAM_MEMBERS);
        await dispatch(FETCH_INVITATIONS);
        commit(SET_TEAM_INITIALIZED);
      } catch (err) {
        const msg = `Error fetching team data for ${getters[TEAM].name}`;
        if (
          err.response &&
          Object.prototype.hasOwnProperty.call(err.response.data, "detail")
        ) {
          throw new Error(`${msg}: ${err.response.data.detail}`);
        } else {
          throw new Error(`${msg}: ${err.message}`);
        }
      }
    }
  },

  async [FETCH_ALL_TENANT_DATA]({ dispatch, getters }) {
    const tenants = getters[TENANTS]; // remember, active team/tenants may have changed by the time function returns

    if (!tenants.length) {
      throw new Error(`The current team has no tenants.`);
    }

    const results = await Promise.allSettled(
      tenants.map((tenant) => dispatch(FETCH_TENANT_SPECIFIC_DATA, tenant))
    );
    return results.map(({ status, value, reason }, index) => {
      return { status, value, reason, tenant: tenants[index].id };
    });
  },

  async [UPDATE_TEAM]({ commit, getters }, teamData) {
    const url = `${getAPIRoute("teams")}${getters[TEAM].id}`;
    const response = await axios.patch(url, teamData);
    const team = response.data;
    commit(MODIFY_TEAM, team);
  },

  async [FETCH_USER]({ commit }) {
    const url = getAPIRoute("userProfile");
    const response = await axios.get(url);
    const user = response.data;
    commit(SET_USER, user);
  },

  async [UPDATE_USER]({ commit }, userData) {
    const url = getAPIRoute("userProfile");
    const response = await axios.patch(url, userData);
    const user = response.data;
    commit(SET_USER, user);
  },
};

export default actions;
