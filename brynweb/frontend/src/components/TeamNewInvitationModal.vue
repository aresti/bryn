<template>
  <base-modal @close-modal="onClose">
    <base-card>
      <div class="content is-size-5 has-text-centered">
        <h4 class="title is-4">Send an Invitation</h4>
        <p>
          Invite a new team member to join <strong>{{ team.name }}</strong>
        </p>
      </div>
      <base-form-validated
        :form="form"
        submitLabel="Send Invitation"
        :submitted="submitted"
        @submit="onSubmit"
      />
    </base-card>
  </base-modal>
</template>

<script>
import { mapActions, mapState, mapGetters } from "vuex";

import useFormValidation from "@/composables/formValidation";
import {
  isRequired,
  isValidEmailSyntax,
  ValidationError,
} from "@/composables/formValidation/validators";

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
        email: {
          label: "Email",
          type: "email",
          validators: [isRequired, isValidEmailSyntax, this.isUniqueEmail],
          iconClasses: ["fa", "fa-envelope"],
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
    ...mapGetters(["team"]),
    ...mapGetters("invitations", ["allInvitations"]),
    invalidEmails() {
      return this.allInvitations.map((invitation) => invitation.email);
    },
  },

  // Non-reactive
  methods: {
    ...mapActions("invitations", ["createInvitation"]),
    isUniqueEmail(value) {
      if (!value || !this.invalidEmails.includes(value)) {
        return true;
      }
      throw new ValidationError(
        "You've already sent an invite to this email address"
      );
    },
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
        const invitation = await this.createInvitation(this.form.values);
        this.toast.success(`Team invitation sent to ${invitation.email}`);
        this.onClose();
      } catch (err) {
        if (err.response?.status === 400) {
          this.form.parseResponseError(err.response.data);
        } else {
          this.toast.error(
            `Failed to send invitation: ${
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