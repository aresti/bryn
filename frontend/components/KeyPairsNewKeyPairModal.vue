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
        :form="form"
        submitLabel="Add Key"
        :submitted="submitted"
        @validate-field="formValidateField"
        @submit="onSubmit"
      />
    </template>
    <template v-slot:right>
      <vue-markdown-it :source="guidance" />
    </template>
  </base-modal-split>
</template>

<script>
import { useToast } from "vue-toastification";
import VueMarkdownIt from "vue3-markdown-it";

import formValidationMixin from "@/mixins/formValidationMixin";
import guidance from "@/content/keypairs/newKeyPairGuidance.md";
import { mapActions, mapState, mapGetters } from "vuex";
import {
  isAlphaNumHyphensOnly,
  isPublicKey,
  isRequired,
  ValidationError,
} from "@/utils/validators";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

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
        publicKey: {
          label: "Public Key",
          value: "",
          element: "textarea",
          errors: [],
          validators: [isRequired, isPublicKey, this.isUniquePublicKey],
        },
        name: {
          label: "Key Name",
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
    ...mapGetters("keyPairs", ["getKeyPairsForTenant"]),
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
    invalidPublicKeys() {
      return this.selectedTenant
        ? this.getKeyPairsForTenant(this.selectedTenant).map(
            (keypair) => keypair.publicKey
          )
        : [];
    },
  },

  methods: {
    ...mapActions("keyPairs", ["createKeyPair"]),
    onClose() {
      this.$emit("close-modal");
    },
    async onSubmit() {
      this.formValidate();
      if (this.submitted || !this.formIsValid) {
        return;
      }
      this.submitted = true;
      try {
        const keypair = await this.createKeyPair(this.formValues);
        this.toast.success(`New SSH key created: ${keypair.name}`);
        this.onClose();
      } catch (err) {
        if (err.response.status === 400) {
          this.formParseResponseError(err.response.data);
        } else {
          this.toast.error(
            `Failed to create SSH key: ${err.response.data.detail}`
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
    isUniquePublicKey(value) {
      if (!value || !this.invalidPublicKeys.includes(value)) {
        return true;
      }
      const existing = this.getKeyPairsForTenant(this.selectedTenant).find(
        (existing) => existing.publicKey === value
      );
      throw new ValidationError(
        `You've already stored this public key as '${existing.name}'`
      );
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
};
</script>