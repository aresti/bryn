import {
  INIT_LICENCE_TERMS,
  INIT_REGIONS,
  INIT_TEAMS,
  INIT_USER,
  MODIFY_TEAM,
  SET_ACTIVE_TEAM_ID,
  SET_FAQS,
  SET_FILTER_TENANT_ID,
  SET_HYPERVISOR_STATS,
  SET_READY,
  SET_TEAM_INITIALIZED,
  SET_USER,
} from "@/store/mutation-types";

const mutations = {
  [INIT_LICENCE_TERMS](state) {
    state.licenceTerms = document.getElementById("licenceTerms").innerHTML;
  },
  [INIT_REGIONS](state) {
    state.regions = JSON.parse(
      document.getElementById("regionsData").textContent
    );
  },

  [INIT_TEAMS](state) {
    const parsed = JSON.parse(document.getElementById("teamsData").textContent);
    parsed.forEach((team) => (team.initialized = false));
    state.teams = parsed;
  },

  [INIT_USER](state) {
    state.user = JSON.parse(document.getElementById("userData").textContent);
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

  [SET_TEAM_INITIALIZED](state) {
    state.teams.find(
      (team) => team.id === state.activeTeamId
    ).initialized = true;
  },

  [SET_USER](state, user) {
    state.user = user;
  },
};

export default mutations;
