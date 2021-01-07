<template>
  <base-modal-split @close-modal="closeModal">
    <template v-slot:left>
      <h4 class="title is-4">Attach {{ volume.name }}</h4>
      <p>
        Attach
        <span class="has-text-weight-semibold is-family-monospace">{{
          volume.name
        }}</span>
        to an instance.
      </p>

      <base-form-validated
        :form="form"
        submitLabel="Attach Volume"
        :submitted="submitted"
        :nonFieldErrors="nonFieldErrors"
        @submit="submitForm"
      />
    </template>

    <template v-slot:right>
      <h4 class="title is-4">Help with attachments</h4>
      <vue-markdown-it :source="guidance" />
    </template>
  </base-modal-split>
</template>

<script>
import formValidationMixin from "@/mixins/formValidationMixin";
import guidance from "@/content/volumes/newVolumeGuidance.md";

import VueMarkdownIt from "vue3-markdown-it";
import { useToast } from "vue-toastification";
import { isRequired } from "@/utils/validators";
import { mapActions, mapGetters } from "vuex";

export default {
  mixins: [formValidationMixin],

  props: {
    volume: {
      type: Object,
      required: true,
    },
  },

  emits: {
    "close-modal": null,
  },

  components: {
    VueMarkdownIt,
  },

  setup() {
    const toast = useToast();
    return { toast };
  },

  data() {
    return {
      guidance,
      form: {
        server: {
          label: "Server",
          element: "select",
          options: [],
          value: "",
          validators: [isRequired],
        },
      },
      nonFieldErrors: [],
      submitted: false,
    };
  },

  computed: {
    ...mapGetters(["getTenantById"]),
    ...mapGetters("instances", ["getInstancesForTenant", "getInstanceById"]),
    serverOptions() {
      /* Active instances for tenant */
      const tenant = this.getTenantById(this.volume.tenant);
      const instances = this.getInstancesForTenant(tenant).filter(
        (instance) => instance.status === "ACTIVE"
      );
      return this.formMapToOptions(instances);
    },
  },

  methods: {
    ...mapActions("volumes", ["attachVolume"]),
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
        const server = this.getInstanceById(this.formValues.server);
        const volume = this.volume;
        await this.attachVolume({ volume, server });
        this.toast.success(
          `Volume '${volume.name}' attached to '${server.name}'`
        );
        this.closeModal();
      } catch (err) {
        if (err.response?.status === 400) {
          this.formParseResponseError(err.response.data);
        } else {
          this.toast.error(
            `Failed to attach volume: ${
              err.response?.data.detail ?? "unexpected error"
            }`
          );
        }
      } finally {
        this.submitted = false;
      }
    },
  },

  mounted() {
    this.form.server.options = this.serverOptions;
  },
};
</script>