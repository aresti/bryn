/**
 * Updates a collection of objects, optionally for a specific tenant only
 *
 * @param {Object[]} collection - The collection to update
 * @param {Object[]} values - The new values
 * @param {Object} [options] - The options object
 * @param {Object} [options.tenant] - The tenant, for which values will be replaced
 * @param {number} [options.tenant.id] - The tenant id
 */
function updateTenantCollection(
  collection,
  values,
  { tenant: { id } = {} } = {}
) {
  if (id == null) {
    // No tenant specified, replace all (maintaining ref to original array)
    collection.splice(0, collection.length, ...values);
  } else {
    // Replace existing values matching tenant (maintain ref to original array)
    const filtered = collection.filter((value) => value.tenant !== id);
    collection.splice(0, collection.length, ...filtered);
    collection.push(...values);
  }
}

export { updateTenantCollection };
