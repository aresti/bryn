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
          <base-level-item>
            <base-button rounded @click="showBootable = !showBootable"
              ><template v-slot:icon-before>
                <base-icon
                  :fa-classes="[
                    'fas',
                    showBootable ? 'fas fa-eye-slash' : 'fas fa-eye',
                  ]"
                  :decorative="true"
                />
              </template>
              <template v-slot:default>{{
                showBootable ? "Hide boot volumes" : "Show boot volumes"
              }}</template>
            </base-button>
          </base-level-item>
          <base-level-item>
            <base-button-create @click="showNewVolumeModal = true">
              New volume
            </base-button-create>
          </base-level-item>
        </template>
      </base-level>
    </div>
    <volumes-table :volumes="filteredVolumes" />

    <base-flex-centered v-if="loading">
      <div class="loader is-loading"></div>
    </base-flex-centered>

    <!-- <key-pairs-new-key-pair-modal
      v-if="showNewVolumeModal"
      @close-modal="showNewVolumeModal = false"
    /> -->
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import { mapGetters, mapState } from "vuex";

// import VolumesNewVolumeModal from "@/components/VolumesNewVolumeModal";
import VolumesTable from "@/components/VolumesTable";
import TenantFilterTabs from "@/components/TenantFilterTabs";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

  components: {
    // VolumesNewVolumeModal,
    VolumesTable,
    TenantFilterTabs,
  },

  data() {
    return {
      showBootable: false,
      showNewVolumeModal: false,
    };
  },

  computed: {
    ...mapState({
      loading: (state) => state.volumes.loading,
    }),
    ...mapGetters("volumes", ["volumesForFilterTenant"]),
    filteredVolumes() {
      return this.showBootable
        ? this.volumesForFilterTenant
        : this.volumesForFilterTenant.filter((volume) => !volume.bootable);
    },
  },
};
</script>

<style scoped>
.loader {
  height: 200px;
  width: 200px;
}
</style>