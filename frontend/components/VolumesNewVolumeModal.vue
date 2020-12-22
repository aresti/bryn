<template>
  <base-modal-split @close-modal="closeModal">
    <template v-slot:left>
      <h4 class="title is-4">Create a New Volume</h4>
      <p>Create a new volume, which can be attached to your instances.</p>

      <base-form-validated
        :form="form"
        :nonFieldErrors="formNonFieldErrors"
        submitLabel="Create Volume"
        :submitted="submitted"
        @validate-field="formValidateField"
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
      <!-- <vue-markdown-it :source="guidance" /> -->
    </template>
  </base-modal-split>
</template>

<script>
import formValidationMixin from "@/mixins/formValidationMixin";
import { formatBytes } from "@/utils";
import {
  isAlphaNumHyphensOnly,
  isRequired,
  ValidationError,
} from "@/utils/validators";
// import guidance from "@/content/instances/newInstanceGuidance.md";

import VueMarkdownIt from "vue3-markdown-it";
import { useToast } from "vue-toastification";
import { mapState, mapActions, mapGetters } from "vuex";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

  mixins: [formValidationMixin],

  emits: {
    "close-modal": null,
  },

  components: {
    VueMarkdownIt,
  },

  data() {
    return {
      // guidance,
      form: {
        tenant: {
          label: "Region",
          element: "select",
          options: [],
          value: "",
          errors: [],
          validators: [isRequired],
        },
        volumeType: {
          label: "Volume Type",
          element: "select",
          options: [],
          value: "",
          errors: [],
          validators: [isRequired],
        },
        size: {
          label: "Size",
          element: "select",
          options: [],
          value: "250",
          errors: [],
          validators: [isRequired],
        },
        name: {
          label: "Name",
          value: "",
          errors: [],
          validators: [isRequired, isAlphaNumHyphensOnly, this.isUniqueName],
        },
      },
      submitted: false,
    };
  },

  computed: {
    ...mapState(["filterTenantId"]),
    ...mapGetters(["tenants", "getTenantById", "getRegionNameForTenant"]),
    ...mapGetters("volumes", ["getVolumesForTenant"]),
    ...mapGetters("volumeTypes", ["getVolumeTypesForTenant"]),
    selectedTenant() {
      return this.form.tenant.value
        ? this.getTenantById(parseInt(this.form.tenant.value))
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

  methods: {
    ...mapActions("volumes", ["createVolume"]),
    closeModal() {
      this.$emit("close-modal");
    },
    async submitForm() {
      this.formValidate();
      if (this.submitted || !this.formIsValid) {
        return;
      }
      this.submitted = true;
      try {
        const volume = await this.createVolume(this.formValues);
        this.toast.success(`New volume created: ${volume.name}`);
        this.closeModal();
      } catch (err) {
        if (err.response?.status === 400) {
          this.formParseResponseError(err.response.data);
        } else {
          console.log(err);
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

  watch: {
    selectedTenant: {
      handler(_new, _old) {
        this.form.volumeType.value = this.defaultVolumeTypeId;
        this.form.volumeType.options = this.formMapToOptions(this.volumeTypes);
      },
      immediate: true,
    },
  },

  mounted() {
    this.form.tenant.options = this.tenantOptions;
    if (this.filterTenantId) {
      this.form.tenant.value = this.filterTenantId;
    } else if (this.tenants.length === 1) {
      this.form.tenant.value = this.tenants[0].id;
    }
    this.form.size.options = this.sizeOptions;
  },
};
</script>