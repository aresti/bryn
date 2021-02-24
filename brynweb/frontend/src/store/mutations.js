import {
  INIT_REGIONS,
  INIT_TEAMS,
  INIT_USER,
  SET_ACTIVE_TEAM_ID,
  SET_FILTER_TENANT_ID,
  SET_HYPERVISOR_STATS,
  SET_TEAM_INITIALIZED,
  MODIFY_TEAM,
  SET_USER,
} from "@/store/mutation-types";

const mutations = {
  [INIT_REGIONS](state) {
    state.regions = JSON.parse(
      document.getElementById("regionsData").textContent
    );
  },

  [INIT_TEAMS](state) {
    state.teams = JSON.parse(document.getElementById("teamsData").textContent);
  },

  [INIT_USER](state) {
    state.user = JSON.parse(document.getElementById("userData").textContent);
  },

  [SET_ACTIVE_TEAM_ID](state, id) {
    state.activeTeamId = id;
  },

  [SET_FILTER_TENANT_ID](state, id) {
    state.filterTenantId = id;
  },

  [SET_HYPERVISOR_STATS](state, hypervisorStats) {
    state.hypervisorStats = hypervisorStats;
  },

  [SET_TEAM_INITIALIZED](state) {
    state.teams.find(
      (team) => team.id === state.activeTeamId
    ).initialized = true;
  },

  [MODIFY_TEAM](state, teamData) {
    const team = state.teams.find((team) => team.id === state.activeTeamId);
    Object.assign(team, teamData);
  },

  [SET_USER](state, user) {
    state.user = user;
  },
};

export default mutations;
