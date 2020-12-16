<template>
  <base-modal-split @close-modal="onClose">
    <template v-slot:left>
      <h4 class="title is-4">Launch new server</h4>
      <p>Create a new server instance.</p>

      <base-form-validated
        :fields="form"
        submitLabel="Launch server"
        @validate-field="validateField"
        @submit="onSubmit"
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

import VueMarkdownIt from "vue3-markdown-it";
import {
  isAlphaNumHyphensOnly,
  isRequired,
  ValidationError,
} from "@/helpers/validators";
import { mapState, mapActions, mapGetters } from "vuex";

const defaultMapToOptions = (entities) => {
  return entities.map((entity) => {
    return {
      value: entity.id,
      label: entity.name,
    };
  });
};

export default {
  mixins: [formValidationMixin],

  emits: {
    "close-modal": null,
  },

  components: {
    VueMarkdownIt,
  },

  data() {
    return {
      guidance,
      form: {
        tenant: {
          label: "Region",
          element: "select",
          options: [],
          value: "",
          errors: [],
          validators: [isRequired],
        },
        flavor: {
          label: "Flavor",
          element: "select",
          options: [],
          value: "",
          errors: [],
          validators: [isRequired],
        },
        image: {
          label: "Image",
          element: "select",
          options: [],
          value: "",
          errors: [],
          validators: [isRequired],
        },
        keypair: {
          label: "SSH Key",
          element: "select",
          options: [],
          value: "",
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
    ...mapState(["filterTenant"]),
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
    imageOptions() {
      return defaultMapToOptions(this.images);
    },
    flavors() {
      return this.selectedTenant
        ? this.getFlavorsForTenant(this.selectedTenant)
        : [];
    },
    flavorOptions() {
      return defaultMapToOptions(this.flavors);
    },
    keypairs() {
      return this.selectedTenant
        ? this.getKeyPairsForTenant(this.selectedTenant)
        : [];
    },
    keypairOptions() {
      return defaultMapToOptions(this.keypairs);
    },
    invalidNames() {
      return this.selectedTenant
        ? this.getInstancesForTenant(this.selectedTenant).map(
            (instance) => instance.name
          )
        : [];
    },
  },

  methods: {
    ...mapActions("instances", ["createInstance"]),
    onClose() {
      this.$emit("close-modal");
    },
    onSubmit() {
      this.validateForm();
    },
    // async onSubmit(values) {
    //   try {
    //     const result = await this.createInstance(values);
    //     console.log(result);
    //   } catch (err) {
    //     console.log(err.response.data.detail);
    //   }
    // },
    isUniqueName(value) {
      if (!value || !this.invalidNames.includes(value)) {
        return true;
      }
      throw new ValidationError("A unique name is required");
    },
  },

  watch: {
    selectedTenant() {
      this.form.flavor.value = "";
      this.form.flavor.options = this.flavorOptions;
      this.form.image.value = "";
      this.form.image.options = this.imageOptions;
      this.form.keypair.value = "";
      this.form.keypair.options = this.keypairOptions;
    },
  },

  mounted() {
    this.form.tenant.value = this.filterTenant ?? "";
    this.form.tenant.options = this.tenantOptions;
  },
};
</script>