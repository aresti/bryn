// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.timeout = 20000;

const baseUrl = "/api";

const apiRoutes = {
  images: baseUrl + "/images/",
  instances: baseUrl + "/instances/",
  invitations: baseUrl + "/invitations/",
  flavors: baseUrl + "/flavors/",
  keyPairs: baseUrl + "/keypairs/",
  team: baseUrl + "/teams/",
  teamMembers: baseUrl + "/teammembers/",
  userProfile: baseUrl + "/userprofile/",
  volumes: baseUrl + "/volumes/",
  volumeTypes: baseUrl + "/volumetypes",
};

export { axios, apiRoutes };
