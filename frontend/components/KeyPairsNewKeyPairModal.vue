<template>
  <base-modal-split @close-modal="onClose">
    <template v-slot:left>
      <h4 class="title is-4">Add new SSH key</h4>
      <p>
        Copy and paste your public SSH key below, and give it a descriptive name
        like
        <span class="is-family-monospace">'simons-hipster-laptop'</span>
      </p>
      <base-form-validated
        :fields="form"
        submitLabel="Add key"
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
import guidance from "@/content/keypairs/newKeyPairGuidance.md";

import VueMarkdownIt from "vue3-markdown-it";
import { mapState, mapGetters } from "vuex";
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
        tenant: {
          label: "Region",
          value: "",
          element: "select",
          options: [],
          errors: [],
          validators: [isRequired],
        },
        pubKey: {
          label: "Public Key",
          value: "",
          element: "textarea",
          errors: [],
          validators: [isRequired, isPublicKey],
        },
        name: {
          label: "Key name",
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
    getTenantOptions() {
      return this.tenants.map((tenant) => {
        return {
          value: tenant.id,
          label: this.getRegionNameForTenant(tenant),
        };
      });
    },
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

  watch: {
    selectedTenant: {
      handler(_new, _old) {
        this.form.tenant.options = this.tenantOptions;
      },
      immediate: true,
    },
  },

  mounted() {
    if (this.filterTenant) {
      this.form.tenant.value = this.filterTenant;
    } else if (this.tenants.length === 1) {
      this.form.tenant.value = this.tenants[0].id;
      this.validateField("tenant");
    }
  },
};
</script>