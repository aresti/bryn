// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.timeout = 15000;

const baseUrl = "/api";
const baseUrlUser = "/user/api";

const apiRoutes = {
  getInstances: baseUrl + "/instances",
  getFlavors: baseUrl + "/flavors",
  getImages: baseUrl + "/images",
  getKeyPairs: baseUrl + "/keypairs",
  getVolumes: baseUrl + "/volumes",
  getTeamMembers: baseUrlUser + "/teammembers/",
  postInstance: baseUrl + "/instances/",
};

export { axios, apiRoutes };
