<template>
  <div>
    <div class="block mb-5">
      <base-level>
        <template v-slot:left>
          <base-level-item>
            <tenant-filter-tabs
              entity-name="Servers"
              v-if="tenants.length > 1"
            />
            <h2 v-else class="title">Servers</h2>
          </base-level-item>
        </template>
        <template v-slot:right>
          <base-mini-loader :loading="loading" />
          <base-level-item v-if="hasShelved">
            <base-button
              class="mr-2"
              rounded
              @click="showShelved = !showShelved"
              color="primary"
              outlined
              ><template v-slot:icon-before>
                <base-icon
                  :icon="['fas', showShelved ? 'eye-slash' : 'eye']"
                  :decorative="true"
                />
              </template>
              <template v-slot:default>{{
                showShelved ? "Hide shelved" : "Show shelved"
              }}</template>
            </base-button>
            <base-button-create
              @click="onNewServerClick"
              :disabled="launchingDisabledAllTenants"
            >
              New server
            </base-button-create>
          </base-level-item>
        </template>
      </base-level>
    </div>

    <div v-if="!loading" class="box">
      <!-- Launching disabled message -->
      <base-message v-if="launchingDisabledAllTenants" color="warning">
        Launching new instances is currently disabled for all regions, due to
        capacity issues.
      </base-message>

      <!-- Instances table -->
      <instances-table
        v-if="instancesForFilterTenant.length"
        :instances="filteredInstances"
      />

      <!-- No instances message -->
      <div v-else class="content has-text-centered">
        <h4 class="subtitle mb-0">{{ noItemsMessage }}</h4>
      </div>
    </div>

    <base-message color="primary">
      <h4 class="subtitle">What is a server lease?</h4>
      <p class="has-text-primary">
        In order to better use the limited capacity accross our CLIMB-BIG-DATA
        infrastructure, we have introduced the concept of server leases. By
        default, leases will last 2 weeks and can be easily renewed. Upon
        expiry, a server is liable to be shelved without notice.
      </p>
      <p class="has-text-primary mt-2">
        If you are running a webserver, or have some other special case, you can
        <a @click="showInstancesIndefiniteLeaseRequestModal = true"
          >request an indefinite lease</a
        >.
      </p>
    </base-message>

    <instances-indefinite-lease-request-modal
      v-if="showInstancesIndefiniteLeaseRequestModal"
      @close-modal="showInstancesIndefiniteLeaseRequestModal = false"
    />

    <instances-new-instance-modal
      v-if="showInstancesNewInstanceModal"
      @close-modal="showInstancesNewInstanceModal = false"
    />

    <key-pairs-new-key-pair-modal
      v-if="showKeyPairsNewKeyPairModal"
      submit-button-text="Add Key and Continue"
      @close-modal="onKeyPairModalClose"
    />
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import {
  FILTER_TENANT,
  GET_REGION_NAME_FOR_TENANT,
  INSTANCES_FOR_FILTER_TENANT,
  LIVE_INSTANCES_FOR_FILTER_TENANT,
  TEAM,
  TENANTS,
} from "@/store/getter-types";

import InstancesIndefiniteLeaseRequestModal from "@/components/InstancesIndefiniteLeaseRequestModal";
import InstancesNewInstanceModal from "@/components/InstancesNewInstanceModal";
import InstancesTable from "@/components/InstancesTable";
import KeyPairsNewKeyPairModal from "@/components/KeyPairsNewKeyPairModal";
import TenantFilterTabs from "@/components/TenantFilterTabs";

export default {
  // Template dependencies
  components: {
    InstancesIndefiniteLeaseRequestModal,
    InstancesTable,
    InstancesNewInstanceModal,
    KeyPairsNewKeyPairModal,
    TenantFilterTabs,
  },

  // Composition
  inject: ["toast"],

  // Local state
  data() {
    return {
      showShelved: false,
      showInstancesIndefiniteLeaseRequestModal: false,
      showKeyPairsNewKeyPairModal: false,
      showInstancesNewInstanceModal: false,
    };
  },

  computed: {
    ...mapState({
      loading: (state) => state.instances.loading,
      keyPairs: (state) => state.keyPairs.all,
    }),
    ...mapGetters({
      filterTenant: FILTER_TENANT,
      getRegionNameForTenant: GET_REGION_NAME_FOR_TENANT,
      instancesForFilterTenant: INSTANCES_FOR_FILTER_TENANT,
      liveInstancesForFilterTenant: LIVE_INSTANCES_FOR_FILTER_TENANT,
      tenants: TENANTS,
    }),
    filteredInstances() {
      return this.showShelved
        ? this.instancesForFilterTenant
        : this.liveInstancesForFilterTenant;
    },
    hasShelved() {
      return (
        this.instancesForFilterTenant.length !==
        this.liveInstancesForFilterTenant.length
      );
    },
    noItemsMessage() {
      if (this.filterTenant != null) {
        return `You haven't created any servers at ${this.getRegionNameForTenant(
          this.filterTenant
        )} yet`;
      } else {
        return "You haven't created any servers yet";
      }
    },
    launchingDisabledAllTenants() {
      return this.tenants.every((tenant) => tenant.disableNewInstances);
    },
  },

  // Events
  // Note, this wont work as a mixin due https://github.com/vuejs/vue-router-next/issues/454
  beforeRouteEnter(to, _from, next) {
    next((vm) => {
      const hasTenants = vm.$store.getters[TENANTS].length;
      const hasLicense = vm.$store.getters[TEAM].licenceIsValid;
      if (!(hasTenants && hasLicense)) {
        // No tenants or no license, redirect to team admin view
        vm.$router.push({
          name: "dashboard",
          params: { teamId: to.params.teamId },
        });
      }
    });
  },

  // Non-reactive
  methods: {
    onNewServerClick() {
      // Handle no-keys for user
      if (this.keyPairs.length) {
        this.showInstancesNewInstanceModal = true;
      } else {
        this.showKeyPairsNewKeyPairModal = true;
      }
    },
    onKeyPairModalClose() {
      this.showKeyPairsNewKeyPairModal = false;
      if (this.keyPairs.length) {
        // User created a keypair, continue to server modal
        this.showInstancesNewInstanceModal = true;
      }
    },
  },
};
</script>