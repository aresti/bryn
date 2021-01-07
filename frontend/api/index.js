// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.timeout = 20000;

const baseUrl = "/api";
const baseUrlUser = "/user/api";

const apiRoutes = {
  images: baseUrl + "/images/",
  instances: baseUrl + "/instances/",
  invitations: baseUrlUser + "/invitations/",
  flavors: baseUrl + "/flavors/",
  keyPairs: baseUrl + "/keypairs/",
  team: baseUrlUser + "/teams/",
  teamMembers: baseUrlUser + "/teammembers/",
  volumes: baseUrl + "/volumes/",
  volumeTypes: baseUrl + "/volumetypes",
};

export { axios, apiRoutes };
