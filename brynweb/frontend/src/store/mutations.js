const mutations = {
  initRegions(state) {
    state.regions = JSON.parse(
      document.getElementById("regionsData").textContent
    );
  },

  initTeams(state) {
    state.teams = JSON.parse(document.getElementById("teamsData").textContent);
  },

  initUser(state) {
    state.user = JSON.parse(document.getElementById("userData").textContent);
  },

  setActiveTeamId(state, id) {
    state.activeTeamId = id;
  },

  setFilterTenantId(state, id) {
    state.filterTenantId = id;
  },

  setTeamInitialized(state) {
    state.teams.find(
      (team) => team.id === state.activeTeamId
    ).initialized = true;
  },

  updateTeam(state, teamData) {
    const team = state.teams.find((team) => team.id === state.activeTeamId);
    Object.assign(team, teamData);
  },

  updateUser(state, user) {
    state.user = user;
  },
};

export default mutations;
