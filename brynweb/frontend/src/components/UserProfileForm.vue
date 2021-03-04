<template>
  <div>
    <h2>User Profile</h2>

    <div class="box">
      <base-message
        v-if="user.profile.newEmailPendingVerification"
        color="warning"
        light
      >
        New email address
        <strong>{{ user.profile.newEmailPendingVerification }}</strong> pending
        verification. Please check your email for a verification link.
      </base-message>

      <base-form-validated
        :form="form"
        @fieldValidate="form.onFieldValidate"
        submitLabel="Update"
        @submit="onSubmit"
        :submitted="submitted"
        requireInput
      />
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import { UPDATE_USER } from "@/store/action-types";

import { isRequired } from "@/composables/formValidation/validators";
import useFormValidation from "@/composables/formValidation";

export default {
  // Composition
  inject: ["toast"],

  // Local state
  data() {
    return {
      form: useFormValidation({
        firstName: {
          label: "First name",
          validators: [isRequired],
        },
        lastName: {
          label: "Last name",
          validators: [isRequired],
        },
        email: {
          label: "Email",
          validators: [isRequired],
        },
      }),
      submitted: false,
    };
  },

  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
  },

  // Events
  mounted() {
    this.form.fields.firstName.value = this.user.firstName;
    this.form.fields.lastName.value = this.user.lastName;
    this.form.fields.email.value = this.user.email;
  },

  // Non-reactive
  methods: {
    ...mapActions({
      updateUser: UPDATE_USER,
    }),

    async onSubmit() {
      this.form.validate();
      if (this.submitted || !this.form.valid) {
        return;
      }
      this.submitted = true;
      try {
        await this.updateUser(this.form.values);
        this.toast.success("User profile saved");
        this.form.fields.email.value = this.user.email;
        this.form.resetValidation();
      } catch (err) {
        if (err.response?.status === 400) {
          this.form.parseResponseError(err.response.data);
        } else {
          this.toast.error(
            `Failed to update user: ${
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