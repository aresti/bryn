// Axios config
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const baseUrl = "/api";

const apiRoutes = {
  getInstances: baseUrl + "/instances",
  getFlavors: baseUrl + "/flavors",
  getImages: baseUrl + "/images",
  getSSHKeys: baseUrl + "/sshkeys",
};

export { axios, apiRoutes };
