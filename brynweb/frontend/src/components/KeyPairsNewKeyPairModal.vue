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
        :submitLabel="submitButtonText"
        :submitted="submitted"
        @submit="onSubmit"
      />
    </template>
    <template v-slot:right>
      <vue-markdown-it :source="guidance" />
    </template>
  </base-modal-split>
</template>

<script>
import useFormValidation from "@/composables/formValidation";
import {
  isAlphaNumHyphensOnly,
  isPublicKey,
  isRequired,
  ValidationError,
} from "@/composables/formValidation/validators";

import VueMarkdownIt from "vue3-markdown-it";
import guidance from "@/content/keypairs/newKeyPairGuidance.md";

import { mapActions, mapState, mapGetters } from "vuex";

export default {
  // Template dependencies
  components: {
    VueMarkdownIt,
  },

  // Interface
  props: {
    submitButtonText: {
      type: String,
      default: "Add Key",
    },
  },

  emits: {
    "close-modal": null,
  },

  data() {
    return {
      guidance,
      form: useFormValidation({
        publicKey: {
          label: "Public Key",
          element: "textarea",
          validators: [isRequired, isPublicKey, this.isUniquePublicKey],
        },
        name: {
          label: "Key Name",
          iconClasses: ["fas", "fa-tag"],
          validators: [isRequired, isAlphaNumHyphensOnly, this.isUniqueName],
        },
      }),
      submitted: false,
    };
  },

  inject: ["toast"],

  computed: {
    ...mapState("keyPairs", {
      keyPairs: (state) => state.all,
    }),
    invalidNames() {
      return this.keyPairs.map((keypair) => keypair.name);
    },
    invalidPublicKeys() {
      return this.keyPairs.map((keypair) => keypair.publicKey);
    },
  },

  methods: {
    ...mapActions("keyPairs", ["createKeyPair"]),
    onClose() {
      this.$emit("close-modal");
    },
    async onSubmit() {
      this.form.validate();
      if (this.submitted || !this.form.valid) {
        return;
      }
      this.submitted = true;
      try {
        const keypair = await this.createKeyPair(this.form.values);
        this.toast.success(`New SSH key created: ${keypair.name}`);
        this.onClose();
      } catch (err) {
        if (err.response?.status === 400) {
          this.form.parseResponseError(err.response.data);
        } else {
          this.toast.error(
            `Failed to create SSH key: ${
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
    isUniquePublicKey(value) {
      if (!value || !this.invalidPublicKeys.includes(value)) {
        return true;
      }
      const existing = this.keyPairs.find(
        (existing) => existing.publicKey === value
      );
      throw new ValidationError(
        `You've already stored this public key as '${existing.name}'`
      );
    },
  },
};
</script>