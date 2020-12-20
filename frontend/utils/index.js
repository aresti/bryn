/**
 * Updates a collection of objects for a team, optionally for a specific tenant
 *
 * @param {Object[]} collection - The collection to update
 * @param {Object[]} values - The new values
 * @param {number} - The team id
 * @param {Object} [options] - The options object
 * @param {Object} [options.tenantId] - The tenant id
 */
function updateTeamCollection(
  collection,
  values,
  { id: teamId },
  { id: tenantId }
) {
  // Replace existing values matching tenant or team (maintain ref to original array)
  const filtered = collection.filter((value) =>
    tenantId ? value.tenant !== tenantId : value.team !== teamId
  );
  collection.splice(0, collection.length, ...filtered);
  collection.push(...values);
}

function collectionForTeamId(collection, id) {
  return collection.filter((item) => item.team === id);
}

function collectionForTenantId(collection, id) {
  return collection.filter((item) => item.tenant === id);
}

function createFilterByIdGetter(collection) {
  return (id) => {
    return collection.find((item) => item.id === id);
  };
}

function createFilterByTenantGetter(collection) {
  return ({ id }) => {
    return collectionForTenantId(collection, id);
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

export {
  createFilterByIdGetter,
  createFilterByTenantGetter,
  collectionForTeamId,
  collectionForTenantId,
  formatBytes,
  minutesSince,
  titleCase,
  updateTeamCollection,
};
