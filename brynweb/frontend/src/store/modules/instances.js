import { axios, getAPIRoute } from "@/api";
import {
  updateTeamCollection,
  collectionForTeamId,
  createFindByIdGetter,
  createFilterByTenantGetter,
} from "@/utils/store";
import {
  CREATE_INSTANCE,
  CREATE_POLLING_TARGET,
  DELETE_INSTANCE,
  FETCH_INSTANCE,
  FETCH_TENANT_INSTANCES,
  REMOVE_INSTANCE_BY_ID,
  TRANSITION_INSTANCE,
} from "../action-types";
import {
  ALL_INSTANCES,
  FILTER_TENANT,
  GET_INSTANCE_BY_ID,
  GET_INSTANCES_FOR_TENANT,
  GET_INSTANCE_IS_POLLING,
  GET_ITEM_IS_POLLING,
  INSTANCES_FOR_FILTER_TENANT,
  LIVE_INSTANCES_FOR_FILTER_TENANT,
  TEAM,
} from "../getter-types";
import {
  ADD_INSTANCE,
  MODIFY_INSTANCE,
  SET_INSTANCES,
  SET_INSTANCES_LOADING,
} from "../mutation-types";

const SHELVED_STATUSES = ["SHELVED", "SHELVED_OFFLOADED"];

const getInstanceDetailUri = (instance) =>
  getAPIRoute("instances", instance.team, instance.tenant) + instance.id;

const state = () => {
  return {
    all: [],
    loading: false,
  };
};

const mutations = {
  [ADD_INSTANCE](state, instance) {
    state.all.unshift(instance);
  },
  [SET_INSTANCES](state, { instances, team, tenant }) {
    updateTeamCollection(state.all, instances, team, tenant);
  },
  [SET_INSTANCES_LOADING](state, loading) {
    state.loading = loading;
  },
  [MODIFY_INSTANCE](state, instance) {
    /* Update an existing instance, maintaining the ref */
    const target = state.all.find((target) => target.id === instance.id);
    if (target) {
      Object.assign(target, instance);
    }
  },
  [REMOVE_INSTANCE_BY_ID](state, id) {
    const index = state.all.findIndex((instance) => instance.id === id);
    if (index >= 0) {
      state.all.splice(index, 1);
    }
  },
};

const getters = {
  [GET_INSTANCE_BY_ID](state) {
    return createFindByIdGetter(state.all);
  },
  [GET_INSTANCE_IS_POLLING](state, _getters, _rootState, rootGetters) {
    return (instance) => rootGetters[GET_ITEM_IS_POLLING](state.all, instance);
  },
  [GET_INSTANCES_FOR_TENANT](state) {
    return createFilterByTenantGetter(state.all);
  },
  [ALL_INSTANCES](state, _getters, rootState) {
    return collectionForTeamId(state.all, rootState.activeTeamId);
  },
  [INSTANCES_FOR_FILTER_TENANT](_state, getters, rootState, rootGetters) {
    return rootState.filterTenantId
      ? getters[GET_INSTANCES_FOR_TENANT](rootGetters[FILTER_TENANT])
      : getters[ALL_INSTANCES];
  },
  [LIVE_INSTANCES_FOR_FILTER_TENANT](_state, getters) {
    return getters[INSTANCES_FOR_FILTER_TENANT].filter(
      ({ status }) => SHELVED_STATUSES.indexOf(status) === -1
    );
  },
};

const actions = {
  async [FETCH_INSTANCE]({ commit }, instance) {
    /* Fetch and update an individual instance */
    const uri = getInstanceDetailUri(instance);
    try {
      const response = await axios.get(uri);
      instance = response.data;
      commit(MODIFY_INSTANCE, instance);
      return instance;
    } catch (err) {
      if (err.response?.status === 404) {
        // Instances is gone; remove from local state
        commit(REMOVE_INSTANCE_BY_ID, instance.id);
      }
      throw err;
    }
  },

  async [CREATE_INSTANCE](
    { commit, dispatch, rootState, state },
    { tenant, keypair, flavor, image, name }
  ) {
    const payload = { tenant, keypair, flavor, image, name };
    const url = getAPIRoute("instances", rootState.activeTeamId, tenant);
    const response = await axios.post(url, payload);
    const instance = response.data;
    commit(ADD_INSTANCE, instance);
    dispatch(CREATE_POLLING_TARGET, {
      collection: state.all,
      item: instance,
      fetchAction: FETCH_INSTANCE,
      targetStatuses: ["ACTIVE", "ERROR"],
    });
    return instance;
  },

  async [TRANSITION_INSTANCE]({ dispatch, state }, { instance, status }) {
    const payload = { status };
    const uri = getInstanceDetailUri(instance);
    await axios.patch(uri, payload);
    dispatch(CREATE_POLLING_TARGET, {
      collection: state.all,
      item: instance,
      fetchAction: FETCH_INSTANCE,
      targetStatuses: [status],
    });
  },

  async [DELETE_INSTANCE]({ dispatch, state }, instance) {
    /* Delete an instance */
    const uri = getInstanceDetailUri(instance);
    await axios.delete(uri);
    dispatch(CREATE_POLLING_TARGET, {
      collection: state.all,
      item: instance,
      fetchAction: FETCH_INSTANCE,
      targetStatuses: [], // gone
    });
  },

  async [FETCH_TENANT_INSTANCES]({ rootGetters, commit }, tenant) {
    commit(SET_INSTANCES_LOADING, true);
    const team = rootGetters[TEAM];
    const url = getAPIRoute("instances", team.id, tenant.id);
    const response = await axios.get(url);
    const instances = response.data;
    commit(SET_INSTANCES, { instances, team, tenant });
    commit(SET_INSTANCES_LOADING, false);
  },
};

export default {
  namespaced: false,
  state,
  getters,
  actions,
  mutations,
};
