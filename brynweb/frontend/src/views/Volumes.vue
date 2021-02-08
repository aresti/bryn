<template>
  <div>
    <div class="block mb-3">
      <!-- Actions & filters level -->
      <base-level>
        <!-- Level left -->
        <template v-slot:left>
          <base-level-item>
            <!-- Tenant filter tabs OR Title-->
            <tenant-filter-tabs
              entity-name="Volumes"
              v-if="tenants.length > 1"
            />
            <h2 v-else class="title">Volumes</h2>
          </base-level-item>
        </template>

        <!-- Level right -->
        <template v-slot:right>
          <!-- Loading indicator -->
          <base-mini-loader :loading="loading" />

          <!-- Show/hide bootable button -->
          <base-level-item>
            <base-button rounded @click="showBootable = !showBootable"
              ><template v-slot:icon-before>
                <base-icon
                  :icon="['fas', showBootable ? 'eye-slash' : 'eye']"
                  :decorative="true"
                />
              </template>
              <template v-slot:default>{{
                showBootable ? "Hide boot volumes" : "Show boot volumes"
              }}</template>
            </base-button>
          </base-level-item>

          <!-- New volume button -->
          <base-level-item>
            <base-button-create @click="showNewVolumeModal = true">
              New volume
            </base-button-create>
          </base-level-item>
        </template>
      </base-level>
    </div>

    <!-- Volumes table -->
    <volumes-table
      :volumes="filteredVolumes"
      @attach-volume="onAttachVolume"
      @delete-volume="onDeleteVolume"
      @detach-volume="onDetachVolume"
    />

    <!-- No volumes message -->
    <div
      v-if="!(loading || filteredVolumes.length)"
      class="content has-text-centered"
    >
      <h4 class="subtitle">{{ noItemsMessage }}</h4>
    </div>

    <!-- New volume modal -->
    <volumes-new-volume-modal
      v-if="showNewVolumeModal"
      @close-modal="showNewVolumeModal = false"
    />

    <!-- Attach volume modal -->
    <volumes-attach-modal
      v-if="attachVolume"
      :volume="attachVolume"
      @close-modal="attachVolume = null"
    />

    <!-- Confirm delete modal -->
    <base-modal-delete
      v-if="confirmDeleteVolume"
      verb="Delete"
      type="volume"
      :name="confirmDeleteVolume.name"
      :processing="deleteProcessing"
      @close-modal="onCancelDelete"
      @confirm-delete="onConfirmDelete"
    />

    <!-- Confirm detach modal -->
    <base-modal-delete
      v-if="confirmDetachVolume"
      verb="Detach"
      type="volume"
      :name="confirmDetachVolume.name"
      :processing="detachProcessing"
      @close-modal="onCancelDetach"
      @confirm-delete="onConfirmDetach"
    />
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

import VolumesAttachModal from "@/components/VolumesAttachModal";
import VolumesNewVolumeModal from "@/components/VolumesNewVolumeModal";
import VolumesTable from "@/components/VolumesTable";
import TenantFilterTabs from "@/components/TenantFilterTabs";

export default {
  // Template dependencies
  components: {
    VolumesAttachModal,
    VolumesNewVolumeModal,
    VolumesTable,
    TenantFilterTabs,
  },

  // Composition
  inject: ["toast"],

  // Local state
  data() {
    return {
      attachVolume: null,
      confirmDeleteVolume: null,
      confirmDetachVolume: null,
      deleteProcessing: false,
      detachProcessing: false,
      showBootable: false,
      showNewVolumeModal: false,
    };
  },

  computed: {
    ...mapState({
      loading: (state) => state.volumes.loading,
    }),
    ...mapGetters(["filterTenant", "getRegionNameForTenant", "tenants"]),
    ...mapGetters("volumes", ["volumesForFilterTenant"]),

    filteredVolumes() {
      return this.showBootable
        ? this.volumesForFilterTenant
        : this.volumesForFilterTenant.filter((volume) => !volume.bootable);
    },
    noItemsMessage() {
      if (this.filterTenant != null) {
        return `You haven't created any volumes at ${this.getRegionNameForTenant(
          this.filterTenant
        )} yet`;
      } else {
        return "You haven't created any volumes yet";
      }
    },
  },

  // Events
  // Note, this wont work as a mixin due https://github.com/vuejs/vue-router-next/issues/454
  beforeRouteEnter(to, _from, next) {
    next((vm) => {
      const hasTenants = vm.$store.getters.tenants.length;
      const hasLicense = true; // TODO: after licensing
      if (!(hasTenants && hasLicense)) {
        // No tenants or no license, redirect to team admin view
        vm.$router.push({ name: "team", params: { teamId: to.params.teamId } });
      }
    });
  },

  // Non-reactive
  methods: {
    ...mapActions("volumes", ["deleteVolume", "detachVolume"]),

    /* Volume attachment */
    onAttachVolume(volume) {
      this.attachVolume = volume;
    },

    /* Volume deletion */
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
          `Failed to delete volume: ${
            err.response?.data.detail ?? "unexpected error"
          }`
        );
      } finally {
        this.confirmDeleteVolume = null;
        this.deleteProcessing = false;
      }
    },

    /* Volume detachment */
    onDetachVolume(volume) {
      this.confirmDetachVolume = volume;
    },

    onCancelDetach() {
      this.confirmDetachVolume = null;
    },

    async onConfirmDetach() {
      if (this.detachProcessing) {
        return;
      }
      const volume = this.confirmDetachVolume;
      this.detachProcessing = true;
      try {
        await this.detachVolume(volume);
        this.toast(`Detached volume: ${volume.name}`);
      } catch (err) {
        this.toast.error(
          `Failed to detach volume: ${
            err.response?.data.detail ?? "unexpected error"
          }`
        );
      } finally {
        this.confirmDetachVolume = null;
        this.detachProcessing = false;
      }
    },
  },
};
</script>