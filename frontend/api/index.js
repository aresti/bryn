// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.timeout = 10000;

const baseUrl = "/api";

const apiRoutes = {
  getInstances: baseUrl + "/instances",
  getFlavors: baseUrl + "/flavors",
  getImages: baseUrl + "/images",
  getKeyPairs: baseUrl + "/keypairs",
  postInstance: baseUrl + "/instances/",
};

export { axios, apiRoutes };
