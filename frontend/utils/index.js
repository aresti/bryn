function debounce(func, wait = 500, early = false) {
  let timeout;
  return function (...args) {
    const context = this;
    const isEarlyEnable = !timeout && early;
    const executor = function () {
      timeout = null;
      !early && func.apply(context, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(executor, wait);
    isEarlyEnable && func.apply(context, args);
  };
}

const titleCase = (str) => {
  return str.replace(/\w\S*/g, (t) => {
    return t.charAt(0).toUpperCase() + t.substr(1).toLowerCase();
  });
};

const formatBytes = (bytes, decimals = 2) => {
  /* Format storage size in bytes to be human friendly */
  if (bytes === 0) return "0 Bytes";

  const k = 1000;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
};

const minutesSince = (datetime) => {
  /* Time in minutes since a given time (or time string) */
  const testTime = typeof datetime == "string" ? new Date(datetime) : datetime;
  return Math.round((new Date() - testTime) / 1000 / 60);
};

export { debounce, formatBytes, minutesSince, titleCase };
