<template>
  <base-modal @close-modal="onClose">
    <base-card>
      <div class="content is-size-5 has-text-centered">
        <h4 class="title is-4">Request an Indefinite Server Lease</h4>
        <p>
          If you have a specific need for an indefinite server lease (a web
          server, for example), please provide details below and we will try to
          accommodate you.
        </p>
      </div>
      <base-form-validated
        :form="form"
        @fieldValidate="form.onFieldValidate"
        submitLabel="Send Request"
        :submitted="submitted"
        @submit="onSubmit"
      />
    </base-card>
  </base-modal>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { SEND_INDEFINITE_SERVER_LEASE_REQUEST } from "@/store/action-types";
import { LIVE_INSTANCES } from "@/store/getter-types";

import useFormValidation from "@/composables/formValidation";
import { mapToFormOptions } from "@/composables/formValidation/utils";
import { isRequired } from "@/composables/formValidation/validators";

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
      form: useFormValidation({
        instance: {
          label: "Server",
          element: "select",
          validators: [isRequired],
        },
        message: {
          label: "Message",
          element: "textarea",
          validators: [isRequired],
        },
      }),
      submitted: false,
    };
  },

  computed: {
    ...mapGetters({
      liveInstances: LIVE_INSTANCES,
    }),
    instanceOptions() {
      return mapToFormOptions(this.liveInstances);
    },
  },

  // Events
  mounted() {
    this.form.fields.instance.options = this.instanceOptions;
  },

  // Non-reactive
  methods: {
    ...mapActions({
      sendIndefiniteServerLeaseRequest: SEND_INDEFINITE_SERVER_LEASE_REQUEST,
    }),
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
        await this.sendIndefiniteServerLeaseRequest(this.form.values);
        this.toast.success(`Indefinite server lease request submitted`);
        this.onClose();
      } catch (err) {
        if (err.response?.status === 400) {
          this.form.parseResponseError(err.response.data);
        } else {
          this.toast.error(
            `Failed to send request: ${
              err.response?.data.detail ?? "unexpected error"
            }`
          );
        }
      } finally {
        this.submitted = false;
      }
    },
  },
};
</script>