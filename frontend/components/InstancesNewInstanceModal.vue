<template>
  <base-modal-split @close-modal="closeModal">
    <template v-slot:left>
      <h4 class="title is-4">Launch new server</h4>
      <p>Create a new server instance.</p>

      <base-form-validated
        :form="form"
        submitLabel="Launch server"
        :submitted="submitted"
        :nonFieldErrors="nonFieldErrors"
        @submit="submitForm"
      />
    </template>
    <template v-slot:right>
      <vue-markdown-it :source="guidance" />
    </template>
  </base-modal-split>
</template>

<script>
import formValidationMixin from "@/mixins/formValidationMixin";
import guidance from "@/content/instances/newInstanceGuidance.md";
import {
  isAlphaNumHyphensOnly,
  isRequired,
  ValidationError,
} from "@/utils/validators";

import VueMarkdownIt from "vue3-markdown-it";
import { mapState, mapActions, mapGetters } from "vuex";

export default {
  // Dependencies
  components: {
    VueMarkdownIt,
  },

  // Composition
  mixins: [formValidationMixin],
  inject: ["toast"],

  // Interface
  emits: {
    "close-modal": null,
  },

  // Local state
  data() {
    return {
      guidance,
      form: {
        tenant: {
          label: "Region",
          element: "select",
          options: [],
          value: "",
          iconClasses: ["fas", "fa-globe-europe"],
          validators: [isRequired],
        },
        flavor: {
          label: "Flavor",
          element: "select",
          options: [],
          value: "",
          iconClasses: ["fas", "fa-server"],
          validators: [isRequired],
        },
        image: {
          label: "Image",
          element: "select",
          options: [],
          value: "",
          iconClasses: ["fas", "fa-save"],
          validators: [isRequired],
        },
        keypair: {
          label: "SSH Key",
          element: "select",
          options: [],
          value: "",
          iconClasses: ["fas", "fa-key"],
          validators: [isRequired],
        },
        name: {
          label: "Name",
          value: "",
          iconClasses: ["fas", "fa-tag"],
          validators: [isRequired, isAlphaNumHyphensOnly, this.isUniqueName],
        },
      },
      nonFieldErrors: [],
      submitted: false,
    };
  },

  computed: {
    ...mapState(["filterTenantId"]),
    ...mapGetters(["tenants", "getTenantById", "getRegionNameForTenant"]),
    ...mapGetters("flavors", ["getFlavorsForTenant"]),
    ...mapGetters("images", ["getImagesForTenant"]),
    ...mapGetters("instances", ["getInstancesForTenant"]),
    ...mapGetters("keyPairs", ["getKeyPairsForTenant"]),

    selectedTenant() {
      return this.form.tenant.value
        ? this.getTenantById(parseInt(this.form.tenant.value))
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
    keypairs() {
      return this.selectedTenant
        ? this.getKeyPairsForTenant(this.selectedTenant)
        : [];
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
      handler(_new, _old) {
        this.form.flavor.value = "";
        this.form.flavor.options = this.formMapToOptions(this.flavors);
        this.form.image.value = "";
        this.form.image.options = this.formMapToOptions(this.images);
        this.form.keypair.value = "";
        this.form.keypair.options = this.formMapToOptions(this.keypairs);
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
  },

  // Non-reactive
  methods: {
    ...mapActions("instances", ["createInstance"]),

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
        const instance = await this.createInstance(this.formValues);
        this.toast.success(`New server created: ${instance.name}`);
        this.closeModal();
      } catch (err) {
        if (err.response?.status === 400) {
          this.formParseResponseError(err.response.data);
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