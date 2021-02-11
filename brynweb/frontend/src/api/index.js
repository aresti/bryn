// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.timeout = 20000;

const apiBase = "/api/";
const teamBase = apiBase + "teams/TEAM_ID/";
const tenantBase = teamBase + "tenants/TENANT_ID/";

const apiRoutes = {
  images: tenantBase + "images/",
  instances: tenantBase + "instances/",
  invitations: teamBase + "invitations/",
  flavors: tenantBase + "flavors/",
  keyPairs: apiBase + "keypairs/",
  messages: apiBase + "messages/",
  teams: apiBase + "teams/",
  teamMembers: teamBase + "members/",
  userProfile: apiBase + "userprofile/",
  volumes: tenantBase + "volumes/",
  volumeTypes: tenantBase + "volumetypes/",
};

const getAPIRoute = (routeName, teamId = null, tenantId = null) => {
  let route = apiRoutes[routeName];
  if (teamId != null) {
    route = route.replace("TEAM_ID", teamId);
  }
  if (tenantId != null) {
    route = route.replace("TENANT_ID", tenantId);
  }
  return route;
};

export { axios, apiRoutes, getAPIRoute };
