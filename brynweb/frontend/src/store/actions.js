import { axios, getAPIRoute } from "@/api";

import {
  CREATE_LICENCE_ACCEPTANCE,
  CREATE_SERVER_LEASE_REQUEST,
  FETCH_ALL_TENANT_DATA,
  FETCH_ANNOUNCEMENTS,
  FETCH_FAQS,
  FETCH_HYPERVISOR_STATS,
  FETCH_INVITATIONS,
  FETCH_KEY_PAIRS,
  FETCH_REGIONS,
  FETCH_TENANT_FLAVORS,
  FETCH_TENANT_IMAGES,
  FETCH_TEAM,
  FETCH_TEAM_MEMBERS,
  FETCH_TEAM_SPECIFIC_DATA,
  FETCH_TEAMS,
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
import {
  GET_REGION_FOR_TENANT,
  GET_REGION_NAME_FOR_TENANT,
  GET_TEAM_BY_ID,
  TEAM,
} from "./getter-types";
import {
  INIT_LICENCE_TERMS,
  MODIFY_TEAM,
  SET_ACTIVE_TEAM_ID,
  SET_HYPERVISOR_STATS,
  SET_FAQS,
  SET_FILTER_TENANT_ID,
  SET_READY,
  SET_REGIONS,
  SET_TEAMS,
  SET_TENANTS_LOADING,
  SET_USER,
} from "./mutation-types";

const actions = {
  async [INIT_STORE]({ commit, dispatch }) {
    /* Initialise store  */
    commit(INIT_LICENCE_TERMS); // embedded in Django template

    // Required in order
    await dispatch(FETCH_USER);
    await dispatch(FETCH_REGIONS),
      // Required before ready
      await Promise.all([dispatch(FETCH_TEAMS), dispatch(FETCH_KEY_PAIRS)]);
    commit(SET_READY);

    // Non-essential, don't wait
    dispatch(FETCH_HYPERVISOR_STATS);
    dispatch(FETCH_ANNOUNCEMENTS);
    dispatch(FETCH_FAQS);
  },

  [SET_ACTIVE_TEAM]({ commit }, team) {
    commit(SET_ACTIVE_TEAM_ID, team.id);
    commit(SET_FILTER_TENANT_ID, null);
  },

  [SET_FILTER_TENANT]({ commit }, tenant) {
    /* allow null/undefined */
    commit(SET_FILTER_TENANT_ID, tenant?.id);
  },

  async [CREATE_LICENCE_ACCEPTANCE]({ dispatch, state }) {
    const url = getAPIRoute("licenceAcceptances", state.activeTeamId);
    await axios.post(url);
    dispatch(FETCH_TEAM);
  },

  async [CREATE_SERVER_LEASE_REQUEST]({ state }, { instance, message }) {
    const url = getAPIRoute(
      "serverLeaseRequest",
      state.activeTeamId,
      instance.tenant,
      instance.id
    );
    await axios.post(url, { message });
  },

  async [FETCH_FAQS]({ commit }) {
    const url = getAPIRoute("faqs");
    const response = await axios.get(url);
    commit(SET_FAQS, response.data);
  },

  async [FETCH_HYPERVISOR_STATS]({ commit }) {
    const url = getAPIRoute("hypervisorStats");
    const response = await axios.get(url);
    const hypervisorStats = response.data;
    commit(SET_HYPERVISOR_STATS, hypervisorStats);
  },

  async [FETCH_REGIONS]({ commit }) {
    const url = getAPIRoute("regions");
    const response = await axios.get(url);
    commit(SET_REGIONS, response.data);
  },

  async [FETCH_TEAM]({ commit, state }) {
    const url = getAPIRoute("teams") + state.activeTeamId;
    const response = await axios.get(url);
    const team = response.data;
    commit(MODIFY_TEAM, team);
  },

  async [FETCH_TEAMS]({ commit, getters }) {
    const url = getAPIRoute("teams");
    const response = await axios.get(url);
    const teams = response.data;
    // Convenience modifications
    teams.forEach((team) => {
      team.initialized = false;
      team.tenants.forEach((tenant) => {
        const region = getters[GET_REGION_FOR_TENANT](tenant);
        tenant.disabled = region.disabled;
        tenant.newInstancesDisabled = region.newInstancesDisabled;
        tenant.unshelvingDisabled = region.unshelvingDisabled;
      });
    });
    commit(SET_TEAMS, teams);
  },

  async [FETCH_TENANT_SPECIFIC_DATA]({ dispatch, getters }, tenant) {
    /* Fetch all tenant-specific data */
    const team = getters[GET_TEAM_BY_ID](tenant.team);
    const fetchAlways = [FETCH_TENANT_INSTANCES, FETCH_TENANT_VOLUMES];
    const fetchOnce = [
      FETCH_TENANT_FLAVORS,
      FETCH_TENANT_IMAGES,
      FETCH_TENANT_VOLUME_TYPES,
    ];
    const fetchActions = team.initialized
      ? fetchAlways
      : [...fetchAlways, ...fetchOnce];
    try {
      await Promise.all(fetchActions.map((action) => dispatch(action, tenant)));
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

  async [FETCH_TEAM_SPECIFIC_DATA]({ dispatch }, team) {
    /* Fetch all team specific data */
    try {
      await Promise.all([
        dispatch(FETCH_TEAM_MEMBERS),
        dispatch(FETCH_INVITATIONS),
      ]);
    } catch (err) {
      const msg = `Error fetching team data for ${team.name}`;
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

  async [FETCH_ALL_TENANT_DATA]({ commit, dispatch }, team) {
    const tenants = team.tenants.filter((tenant) => !tenant.disabled);
    if (!tenants.length) {
      return {};
    }
    commit(SET_TENANTS_LOADING, true);
    const results = await Promise.allSettled(
      tenants.map((tenant) => dispatch(FETCH_TENANT_SPECIFIC_DATA, tenant))
    );
    commit(SET_TENANTS_LOADING, false);
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

  async [UPDATE_USER](
    { commit },
    { firstName, lastName, email, defaultTeamMembership }
  ) {
    const url = getAPIRoute("userProfile");
    const payload = {
      firstName,
      lastName,
      email,
      profile: { defaultTeamMembership },
    };
    const response = await axios.patch(url, payload);
    const user = response.data;
    commit(SET_USER, user);
  },
};

export default actions;
