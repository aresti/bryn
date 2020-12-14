// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.timeout = 15000;

const baseUrl = "/api";
const baseUrlUser = "/user/api";

const apiRoutes = {
  instances: baseUrl + "/instances/",
  flavors: baseUrl + "/flavors/",
  images: baseUrl + "/images/",
  keyPairs: baseUrl + "/keypairs/",
  volumes: baseUrl + "/volumes/",
  teamMembers: baseUrlUser + "/teammembers/",
};

export { axios, apiRoutes };
