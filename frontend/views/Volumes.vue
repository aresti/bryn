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

    <volumes-table :volumes="filteredVolumes" @delete-volume="onDeleteVolume" />

    <volumes-new-volume-modal
      v-if="showNewVolumeModal"
      @close-modal="showNewVolumeModal = false"
    />

    <base-modal-delete
      v-if="confirmDeleteVolume"
      verb="Delete"
      type="volume"
      :name="confirmDeleteVolume.name"
      :processing="deleteProcessing"
      @close-modal="onCancelDelete"
      @confirm-delete="onConfirmDelete"
    />
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import { mapActions, mapGetters, mapState } from "vuex";

// import VolumesNewVolumeModal from "@/components/VolumesNewVolumeModal";
import VolumesNewVolumeModal from "@/components/VolumesNewVolumeModal";
import VolumesTable from "@/components/VolumesTable";
import TenantFilterTabs from "@/components/TenantFilterTabs";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

  components: {
    VolumesNewVolumeModal,
    VolumesTable,
    TenantFilterTabs,
  },

  data() {
    return {
      showBootable: false,
      showNewVolumeModal: false,
      confirmDeleteVolume: null,
      deleteProcessing: false,
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

  methods: {
    ...mapActions("volumes", ["deleteVolume"]),
    onDeleteVolume(volume) {
      this.confirmDeleteVolume = volume;
    },
    onCancelDelete() {
      this.confirmDeleteVolume = null;
    },
    async onConfirmDelete() {
      if (this.deleteProcessing) {
        return;
      }
      const volume = this.confirmDeleteVolume;
      this.deleteProcessing = true;
      try {
        await this.deleteVolume(volume);
        this.toast(`Deleted volume: ${volume.name}`);
      } catch (err) {
        this.toast.error(
          `Failed to delete volume: ${err.response.data.detail}`
        );
      } finally {
        this.confirmDeleteVolume = null;
        this.deleteProcessing = false;
      }
    },
  },
};
</script>