<template>
  <base-modal-split @close-modal="closeModal">
    <template v-slot:left>
      <h4 class="title is-4">Launch new server</h4>
      <p>Create a new server instance.</p>

      <base-form-validated
        :form="form"
        @fieldValidate="form.onFieldValidate"
        submitLabel="Launch server"
        :submitted="submitted"
        @submit="submitForm"
      />
    </template>
    <template v-slot:right>
      <div v-html="guidanceHTML"></div>
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

import marked from "marked";
import DOMPurify from "dompurify";
import guidanceMarkdown from "@/content/instances/newInstanceGuidance.md";

import { mapState, mapActions, mapGetters } from "vuex";
import { CREATE_INSTANCE } from "@/store/action-types";
import {
  DEFAULT_KEY_PAIR,
  GET_FLAVORS_FOR_TENANT,
  GET_IMAGES_FOR_TENANT,
  GET_INSTANCES_FOR_TENANT,
  GET_REGION_NAME_FOR_TENANT,
  GET_TENANT_BY_ID,
  TENANTS,
} from "@/store/getter-types";

export default {
  // Composition
  inject: ["toast"],

  // Interface
  emits: {
    "close-modal": null,
  },

  // Local state
  data() {
    return {
      guidanceHTML: DOMPurify.sanitize(marked(guidanceMarkdown)),
      form: useFormValidation({
        tenant: {
          label: "Region",
          element: "select",
          iconClasses: ["fas", "globe-europe"],
          validators: [isRequired],
        },
        flavor: {
          label: "Flavor",
          element: "select",
          iconClasses: ["fas", "server"],
          validators: [isRequired],
        },
        image: {
          label: "Image",
          element: "select",
          iconClasses: ["fas", "save"],
          validators: [isRequired],
        },
        keypair: {
          label: "SSH Key",
          element: "select",
          iconClasses: ["fas", "key"],
          validators: [isRequired],
        },
        name: {
          label: "Name",
          iconClasses: ["fas", "tag"],
          validators: [isRequired, isAlphaNumHyphensOnly, this.isUniqueName],
        },
      }),
      submitted: false,
    };
  },

  computed: {
    ...mapState({
      filterTenantId: (state) => state.filterTenantId,
      keyPairs: (state) => state.keyPairs.all,
    }),
    ...mapGetters({
      tenants: TENANTS,
      getTenantById: GET_TENANT_BY_ID,
      getRegionNameForTenant: GET_REGION_NAME_FOR_TENANT,
      getFlavorsForTenant: GET_FLAVORS_FOR_TENANT,
      getImagesForTenant: GET_IMAGES_FOR_TENANT,
      getInstancesForTenant: GET_INSTANCES_FOR_TENANT,
      defaultKeyPair: DEFAULT_KEY_PAIR,
    }),

    selectedTenant() {
      return this.form.fields.tenant.value
        ? this.getTenantById(this.form.fields.tenant.value)
        : null;
    },
    tenantOptions() {
      return this.tenants.map((tenant) => {
        return {
          value: tenant.id,
          label: this.getRegionNameForTenant(tenant),
        };
      });
    },
    images() {
      return this.selectedTenant
        ? this.getImagesForTenant(this.selectedTenant)
        : [];
    },
    flavors() {
      return this.selectedTenant
        ? this.getFlavorsForTenant(this.selectedTenant)
        : [];
    },
    flavorOptions() {
      return this.flavors.map((flavor) => {
        return {
          value: flavor.id,
          label: `${flavor.name} (${flavor.vcpus} vCPUs, ${
            flavor.ram / 1024
          } GB RAM)`,
        };
      });
    },
    invalidNames() {
      return this.selectedTenant
        ? this.getInstancesForTenant(this.selectedTenant).map(
            (instance) => instance.name
          )
        : [];
    },
  },

  // Events
  watch: {
    selectedTenant: {
      handler() {
        this.form.fields.flavor.value = "";
        this.form.fields.flavor.options = this.flavorOptions;
        this.form.fields.image.value = "";
        this.form.fields.image.options = mapToFormOptions(this.images);
      },
      immediate: true,
    },

    kayPairs: {
      handler() {
        this.form.fields.keypair.options = mapToFormOptions(this.keyPairs);
      },
      immediate: true,
    },

    defaultKeyPair: {
      handler() {
        this.form.fields.keypair.value = this.defaultKeyPair?.id ?? "";
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
  },

  // Non-reactive
  methods: {
    ...mapActions({
      createInstance: CREATE_INSTANCE,
    }),

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
        const instance = await this.createInstance(this.form.values);
        this.toast.success(`New server created: ${instance.name}`);
        this.closeModal();
      } catch (err) {
        if (err.response?.status === 400) {
          this.form.parseResponseError(err.response.data);
        } else {
          this.toast.error(
            `Failed to create server: ${
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