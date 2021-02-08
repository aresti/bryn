<template>
  <base-modal-split @close-modal="closeModal">
    <template v-slot:left>
      <h4 class="title is-4">Create a New Volume</h4>
      <p>Create a new volume, which can be attached to your instances.</p>

      <base-form-validated
        :form="form"
        submitLabel="Create Volume"
        :submitted="submitted"
        @submit="submitForm"
      />
    </template>
    <template v-slot:right>
      <h4 class="title is-4">Help with Volumes</h4>
      <base-message color="danger"
        ><strong>Important!</strong><br />As per the user agreement, we cannot
        guarantee the integrity or availability of your data. It is essential
        that you backup your data elsewhere.</base-message
      >
      <vue-markdown-it :source="guidance" />
    </template>
  </base-modal-split>
</template>

<script>
import useFormValidation from "@/composables/formValidation";
import { mapToFormOptions } from "@/composables/formValidation/utils";
import {
  isAlphaNumHyphensOnly,
  isRequired,
  ValidationError,
} from "@/composables/formValidation/validators";

import { formatBytes } from "@/utils";

import guidance from "@/content/volumes/newVolumeGuidance.md";
import VueMarkdownIt from "vue3-markdown-it";

import { mapState, mapActions, mapGetters } from "vuex";

export default {
  // Template dependencies
  components: {
    VueMarkdownIt,
  },

  // Composition
  inject: ["toast"],

  // Interface
  emits: {
    "close-modal": null,
  },

  // Local state
  data() {
    return {
      guidance,
      form: useFormValidation({
        tenant: {
          label: "Region",
          element: "select",
          iconClasses: ["fas", "fa-globe-europe"],
          validators: [isRequired],
        },
        volumeType: {
          label: "Volume Type",
          element: "select",
          iconClasses: ["fas", "fa-hdd"],
          validators: [isRequired],
        },
        size: {
          label: "Size",
          element: "select",
          value: "250",
          iconClasses: ["fas", "fa-save"],
          validators: [isRequired],
        },
        name: {
          label: "Name",
          iconClasses: ["fas", "fa-tag"],
          validators: [isRequired, isAlphaNumHyphensOnly, this.isUniqueName],
        },
      }),
      submitted: false,
    };
  },

  computed: {
    ...mapState(["filterTenantId"]),
    ...mapGetters(["tenants", "getTenantById", "getRegionNameForTenant"]),
    ...mapGetters("volumes", ["getVolumesForTenant"]),
    ...mapGetters("volumeTypes", ["getVolumeTypesForTenant"]),

    selectedTenant() {
      return this.form.fields.tenant.value
        ? this.getTenantById(this.form.fields.tenant.value)
        : null;
    },

    sizeOptions() {
      return [250, 500, 1000, 2000, 5000, 10000, 20000].map((size) => {
        return {
          value: size,
          label: formatBytes(size * Math.pow(1000, 3)),
        };
      });
    },

    tenantOptions() {
      return this.tenants.map((tenant) => {
        return {
          value: tenant.id,
          label: this.getRegionNameForTenant(tenant),
        };
      });
    },

    volumeTypes() {
      return this.selectedTenant
        ? this.getVolumeTypesForTenant(this.selectedTenant)
        : [];
    },

    defaultVolumeTypeId() {
      return this.volumeTypes.find((vt) => vt.isDefault === true)?.id;
    },

    invalidNames() {
      return this.selectedTenant
        ? this.getVolumesForTenant(this.selectedTenant).map(
            (volume) => volume.name
          )
        : [];
    },
  },

  // Events
  watch: {
    selectedTenant: {
      handler(_new, _old) {
        this.form.fields.volumeType.value = this.defaultVolumeTypeId;
        this.form.fields.volumeType.options = mapToFormOptions(
          this.volumeTypes
        );
      },
      immediate: true,
    },
  },

  mounted() {
    this.form.fields.tenant.options = this.tenantOptions;
    if (this.filterTenantId) {
      this.form.fields.tenant.value = this.filterTenantId;
    } else if (this.tenants.length === 1) {
      this.form.fields.tenant.value = this.tenants[0].id;
    }
    this.form.fields.size.options = this.sizeOptions;
  },

  // Non-reactive
  methods: {
    ...mapActions("volumes", ["createVolume"]),

    closeModal() {
      this.$emit("close-modal");
    },

    async submitForm() {
      this.form.validate();
      if (this.submitted || !this.form.valid) {
        return;
      }
      this.submitted = true;
      try {
        const volume = await this.createVolume(this.form.values);
        this.toast.success(`New volume created: ${volume.name}`);
        this.closeModal();
      } catch (err) {
        if (err.response?.status === 400) {
          this.form.parseResponseError(err.response.data);
        } else {
          this.toast.error(
            `Failed to create volume: ${
              err.response?.data.detail ?? "unexpected error"
            }`
          );
        }
      } finally {
        this.submitted = false;
      }
    },

    isUniqueName(value) {
      if (!value || !this.invalidNames.includes(value)) {
        return true;
      }
      throw new ValidationError("A unique name is required");
    },
  },
};
</script>