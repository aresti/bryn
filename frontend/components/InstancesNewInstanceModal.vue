<template>
  <base-modal-split @close-modal="onClose">
    <template v-slot:left>
      <h4 class="title is-4">Launch new server</h4>
      <p>Create a new server instance.</p>

      <form @submit.prevent="onSubmit" novalidate>
        <base-form-control label="Region" :errors="form.tenant.errors" expanded>
          <base-form-field-select
            v-model="form.tenant.value"
            name="tenant"
            :options="tenantOptions"
            null-option-label="Select a region"
            @validate="validateField"
            :invalid="!form.tenant.valid"
            fullwidth
          />
        </base-form-control>

        <fieldset :disabled="!form.tenant.valid">
          <base-form-control
            label="Flavor"
            :errors="form.flavor.errors"
            expanded
          >
            <base-form-field-select
              v-model="form.flavor.value"
              name="flavor"
              :options="flavorOptions"
              null-option-label="Select a flavor"
              @validate="validateField"
              :invalid="!form.flavor.valid"
              fullwidth
            />
          </base-form-control>

          <base-form-control label="Image" :errors="form.image.errors" expanded>
            <base-form-field-select
              v-model="form.image.value"
              name="image"
              :options="imageOptions"
              null-option-label="Select an image"
              @validate="validateField"
              :invalid="!form.image.valid"
              fullwidth
            />
          </base-form-control>

          <base-form-control
            label="SSH Key"
            :errors="form.keypair.errors"
            expanded
          >
            <base-form-field-select
              v-model="form.keypair.value"
              name="keypair"
              :options="keypairOptions"
              null-option-label="Select an keypair"
              @validate="validateField"
              :invalid="!form.keypair.valid"
              fullwidth
            />
          </base-form-control>
        </fieldset>

        <base-form-control label="Server name" :errors="form.name.errors">
          <base-form-field
            v-model="form.name.value"
            name="name"
            type="text"
            placeholder="e.g., my-server-name"
            @validate="validateField"
            :invalid="!form.name.valid"
          />
        </base-form-control>

        <base-button-confirm :loading="submitted" :disabled="!formValid"
          >Launch server</base-button-confirm
        >
      </form>
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
import { mapActions, mapGetters } from "vuex";

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
      form: this.getCleanFormState(),
      submitted: false,
    };
  },

  computed: {
    ...mapGetters(["tenants", "getTenantById", "getRegionNameForTenant"]),
    ...mapGetters("flavors", ["getFlavorsForTenant"]),
    ...mapGetters("images", ["getImagesForTenant"]),
    ...mapGetters("instances", ["getInstancesForTenant"]),
    ...mapGetters("keypairs", ["getKeyPairsForTenant"]),
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
    getCleanFormState() {
      return {
        tenant: { value: "", errors: [], validators: [isRequired] },
        flavor: { value: "", errors: [], validators: [isRequired] },
        image: { value: "", errors: [], validators: [isRequired] },
        keypair: { value: "", errors: [], validators: [isRequired] },
        name: {
          value: "",
          errors: [],
          validators: [isRequired, isAlphaNumHyphensOnly, this.isUniqueName],
        },
      };
    },
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
    selectedtenant() {
      // Clear dependent selections on tenant change
      const freshState = this.getCleanFormState();
      delete freshState.tenant;
      delete freshState.name;
      Object.assign(this.form, freshState);
    },
  },
};
</script>