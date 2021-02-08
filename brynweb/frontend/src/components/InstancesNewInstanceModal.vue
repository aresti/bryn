<template>
  <base-modal-split @close-modal="closeModal">
    <template v-slot:left>
      <h4 class="title is-4">Launch new server</h4>
      <p>Create a new server instance.</p>

      <base-form-validated
        :form="form"
        submitLabel="Launch server"
        :submitted="submitted"
        @submit="submitForm"
      />
    </template>
    <template v-slot:right>
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

import VueMarkdownIt from "vue3-markdown-it";
import guidance from "@/content/instances/newInstanceGuidance.md";

import { mapState, mapActions, mapGetters } from "vuex";

export default {
  // Dependencies
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
    ...mapState(["filterTenantId"]),
    ...mapState("keyPairs", {
      keyPairs: (state) => state.all,
    }),
    ...mapGetters(["tenants", "getTenantById", "getRegionNameForTenant"]),
    ...mapGetters("flavors", ["getFlavorsForTenant"]),
    ...mapGetters("images", ["getImagesForTenant"]),
    ...mapGetters("instances", ["getInstancesForTenant"]),
    ...mapGetters("keyPairs", ["defaultKeyPair"]),

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
        this.form.fields.flavor.options = mapToFormOptions(this.flavors);
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
    ...mapActions("instances", ["createInstance"]),

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