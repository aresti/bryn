<template>
  <base-modal-split @close-modal="onClose">
    <template v-slot:left>
      <h4 class="title is-4">Add new SSH key</h4>
      <p>
        Copy and paste your public SSH key below, and give it a descriptive name
        like
        <span class="is-family-monospace">'simons-hipster-laptop'</span>
      </p>

      <form @submit.prevent="onSubmit" novalidate>
        <base-form-control label="Region" :errors="form.tenant.errors">
          <base-form-field-select
            v-model="form.tenant.value"
            name="tenant"
            :options="tenantOptions"
            null-option-label="Select a region"
            @validate="validateField"
            :invalid="form.tenant.errors?.length"
          />
        </base-form-control>

        <base-form-control label="Public key" :errors="form.pubKey.errors">
          <base-form-field
            v-model="form.pubKey.value"
            name="pubKey"
            element="textarea"
            @validate="validateField"
            :invalid="form.pubKey.errors?.length"
          />
        </base-form-control>

        <base-form-control label="Key name" :errors="form.name.errors">
          <base-form-field
            v-model="form.name.value"
            name="name"
            type="text"
            placeholder="e.g., simons-work-laptop"
            @validate="validateField"
            :invalid="form.name.errors?.length"
          />
        </base-form-control>

        <base-button-confirm :loading="submitted" :disabled="!formValid"
          >Add key</base-button-confirm
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
import guidance from "@/content/keypairs/newKeyPairGuidance.md";

import VueMarkdownIt from "vue3-markdown-it";
import { mapGetters } from "vuex";
import {
  isAlphaNumHyphensOnly,
  isPublicKey,
  isRequired,
  ValidationError,
} from "@/helpers/validators";

export default {
  components: {
    VueMarkdownIt,
  },

  mixins: [formValidationMixin],

  emits: {
    "close-modal": null,
  },

  data() {
    return {
      guidance,
      form: {
        tenant: { value: "", errors: [], validators: [isRequired] },
        name: {
          value: "",
          errors: [],
          validators: [isRequired, isAlphaNumHyphensOnly, this.isUniqueName],
        },
        pubKey: {
          value: "",
          errors: [],
          validators: [isRequired, isPublicKey],
        },
      },
      submitted: false,
    };
  },

  computed: {
    ...mapGetters(["tenants", "getTenantById", "getRegionNameForTenant"]),
    ...mapGetters("keypairs", ["getKeyPairsForTenant"]),
    selectedTenant() {
      return this.getTenantById(parseInt(this.form.tenant.value));
    },
    tenantOptions() {
      return this.tenants.map((tenant) => {
        return {
          value: tenant.id,
          label: this.getRegionNameForTenant(tenant),
        };
      });
    },
    invalidNames() {
      return this.selectedTenant
        ? this.getKeyPairsForTenant(this.selectedTenant).map(
            (keypair) => keypair.name
          )
        : [];
    },
  },

  methods: {
    onClose() {
      this.$emit("close-modal");
    },
    onSubmit() {
      this.validateForm();
    },
    isUniqueName(value) {
      if (!value || !this.invalidNames.includes(value)) {
        return true;
      }
      throw new ValidationError("A unique name is required");
    },
  },

  mounted() {
    if (this.tenants.length === 1) {
      this.form.tenant.value = this.tenants[0].id;
      this.validateField("tenant");
    }
  },
};
</script>