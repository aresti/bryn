import {
  INIT_LICENCE_TERMS,
  MODIFY_TEAM,
  SET_ACTIVE_TEAM_ID,
  SET_FAQS,
  SET_FILTER_TENANT_ID,
  SET_HYPERVISOR_STATS,
  SET_READY,
  SET_REGIONS,
  SET_TEAM_INITIALIZED,
  SET_TEAMS,
  SET_TENANTS_LOADING,
  SET_USER,
} from "@/store/mutation-types";

const mutations = {
  [INIT_LICENCE_TERMS](state) {
    state.licenceTerms = document.getElementById("licenceTerms").innerHTML;
  },

  [MODIFY_TEAM](state, teamData) {
    const team = state.teams.find((team) => team.id === state.activeTeamId);
    Object.assign(team, teamData);
  },

  [SET_ACTIVE_TEAM_ID](state, id) {
    state.activeTeamId = id;
  },

  [SET_FAQS](state, faqs) {
    state.faqs = faqs;
  },

  [SET_FILTER_TENANT_ID](state, id) {
    state.filterTenantId = id;
  },

  [SET_HYPERVISOR_STATS](state, hypervisorStats) {
    state.hypervisorStats = hypervisorStats;
  },

  [SET_READY](state) {
    state.ready = true;
  },

  [SET_REGIONS](state, regions) {
    state.regions = regions;
  },

  [SET_TEAM_INITIALIZED](state, team) {
    const teamId = team.id;
    state.teams.find((team) => team.id === teamId).initialized = true;
  },

  [SET_TEAMS](state, teams) {
    state.teams = teams;
  },

  [SET_TENANTS_LOADING](state, loading) {
    state.tenantsLoading = loading;
  },

  [SET_USER](state, user) {
    state.user = user;
  },
};

export default mutations;
