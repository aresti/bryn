<template>
  <div>
    <div class="block mb-3">
      <base-level>
        <template v-slot:left>
          <base-level-item>
            <tenant-filter-tabs />
          </base-level-item>
        </template>
        <template v-slot:right>
          <base-mini-loader :loading="loading" />
          <base-level-item v-if="hasShelved">
            <base-button rounded @click="showShelved = !showShelved"
              ><template v-slot:icon-before>
                <base-icon
                  :fa-classes="[
                    'fas',
                    showShelved ? 'fas fa-eye-slash' : 'fas fa-eye',
                  ]"
                  :decorative="true"
                />
              </template>
              <template v-slot:default>{{
                showShelved ? "Hide shelved" : "Show shelved"
              }}</template>
            </base-button>
          </base-level-item>
          <base-level-item>
            <base-button-create @click="showInstancesNewInstanceModal = true">
              New server
            </base-button-create>
          </base-level-item>
        </template>
      </base-level>
    </div>
    <instances-table :instances="filteredInstances" />

    <instances-new-instance-modal
      v-if="showInstancesNewInstanceModal"
      @closeModal="showInstancesNewInstanceModal = false"
    />
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import { mapGetters, mapState } from "vuex";

import InstancesNewInstanceModal from "@/components/InstancesNewInstanceModal";
import InstancesTable from "@/components/InstancesTable";
import TenantFilterTabs from "@/components/TenantFilterTabs";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

  components: {
    TenantFilterTabs,
    InstancesTable,
    InstancesNewInstanceModal,
  },

  data() {
    return {
      showShelved: false,
      showInstancesNewInstanceModal: false,
    };
  },

  computed: {
    ...mapState({
      loading: (state) => state.instances.loading,
    }),
    ...mapGetters("instances", [
      "instancesForFilterTenant",
      "notShelvedForFilterTenant",
    ]),
    filteredInstances() {
      return this.showShelved
        ? this.instancesForFilterTenant
        : this.notShelvedForFilterTenant;
    },
    hasShelved() {
      return (
        this.instancesForFilterTenant.length !==
        this.notShelvedForFilterTenant.length
      );
    },
  },
};
</script>