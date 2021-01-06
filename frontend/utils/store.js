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

function addTargetMutation(state, { entity, status = null }) {
  /*
   * Adds a polling target object to state.pollingTargets
   */
  const targets = state.pollingTargets;
  const existingTarget = targets.find((target) => target.id === entity.id);
  if (existingTarget) {
    /* Don't add duplicate targets; update status only */
    existingTarget.status = status;
  } else {
    targets.push({ id: entity.id, status });
  }
}

function removeTargetMutation(state, id) {
  state.pollingTargets.splice(
    state.pollingTargets.findIndex((obj) => obj.id === id),
    1
  );
}

function setSymbolMutation(state, symbol) {
  state.pollingSymbol = symbol;
}

function clearSymbolMutation(state) {
  state.pollingSymbol = null;
}

function addTargetAction(
  { state, commit, dispatch },
  { entity, status, fetchActionName }
) {
  commit("pollingAddTarget", { entity, status });
  dispatch("pollingFetchTargets", { fetchActionName }); // First/immediate update
  if (!state.pollingSymbol) {
    /* Start polling */
    const pollingSymbol = setInterval(() => {
      dispatch("pollingFetchTargets", { fetchActionName });
    }, 5000);
    commit("pollingSetSymbol", pollingSymbol);
  }
}

async function fetchTargetsAction(
  { commit, dispatch, state },
  { fetchActionName }
) {
  /* Fetch & update all polling targets */
  const results = await Promise.allSettled(
    state.pollingTargets.map((target) => {
      const entity = state.all.find((entity) => entity.id === target.id);
      return dispatch(fetchActionName, entity);
    })
  );

  /* Check for 404 (deleted): remove polling targets and volumes*/
  results.forEach((result, index) => {
    if (result.status == "rejected" && result.reason.response?.status === 404) {
      const id = state.pollingTargets[index].id;
      commit("pollingRemoveTarget", id);
      state.all.splice(
        state.all.findIndex((obj) => obj.id === id),
        1
      );
    }
  });

  /* Remove fulfilled polling targets */
  dispatch("pollingRemoveFulfilled");
}

function removeFulfilledAction({ commit, state }) {
  /* Remove any polling targets, where the entity has reached target status */
  for (let i = state.pollingTargets.length - 1; i >= 0; i--) {
    const target = state.pollingTargets[i];
    const entity = state.all.find((entity) => entity.id === target.id);
    const status =
      typeof target.status == "string" ? [target.status] : target.status;

    if (status == null) {
      // resolves by 404, skip this test
      continue;
    }

    if (status.includes(entity.status)) {
      commit("pollingRemoveTarget", entity.id);
    }
  }
  if (!state.pollingTargets.length) {
    /* Stop polling */
    clearInterval(state.pollingSymbol);
    commit("pollingClearSymbol");
  }
}

function createEntityIsPollingGetter(state) {
  return (entity) =>
    state.pollingTargets.some((target) => target.id === entity.id);
}

const pollingUtils = {
  createEntityIsPollingGetter,
  addTargetMutation,
  clearSymbolMutation,
  removeTargetMutation,
  setSymbolMutation,
  addTargetAction,
  fetchTargetsAction,
  removeFulfilledAction,
};

export {
  pollingUtils,
  createFilterByIdGetter,
  createFilterByTenantGetter,
  collectionForTeamId,
  collectionForTenantId,
  updateTeamCollection,
};
