// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.timeout = 15000;

const baseUrl = "/api";
const baseUrlUser = "/user/api";

const apiRoutes = {
  images: baseUrl + "/images/",
  instances: baseUrl + "/instances/",
  flavors: baseUrl + "/flavors/",
  keyPairs: baseUrl + "/keypairs/",
  teamMembers: baseUrlUser + "/teammembers/",
  volumes: baseUrl + "/volumes/",
  volumeTypes: baseUrl + "/volumetypes",
};

export { axios, apiRoutes };
