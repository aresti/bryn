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
import { mapActions, mapGetters, mapState } from "vuex";
import { UPDATE_USER } from "@/store/action-types";
import { GET_TEAM_BY_ID } from "@/store/getter-types";

import {
  isRequired,
  isValidEmailSyntax,
} from "@/composables/formValidation/validators";
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
          validators: [isRequired, isValidEmailSyntax],
        },
        defaultTeamMembership: {
          label: "Default Team",
          element: "select",
        },
      }),
      submitted: false,
    };
  },

  computed: {
    ...mapState({
      user: (state) => state.user,
    }),

    ...mapGetters({
      getTeamById: GET_TEAM_BY_ID,
    }),

    defaultTeamMembershipOptions() {
      return this.user.teamMemberships.map((membership) => {
        return {
          value: membership.id,
          label: this.getTeamById(membership.team)?.name,
        };
      });
    },
  },

  // Events
  mounted() {
    this.form.fields.firstName.value = this.user.firstName;
    this.form.fields.lastName.value = this.user.lastName;
    this.form.fields.email.value = this.user.email;
    this.form.fields.defaultTeamMembership.options = this.defaultTeamMembershipOptions;
    this.form.fields.defaultTeamMembership.value = this.user.profile.defaultTeamMembership;
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
        const {
          firstName,
          lastName,
          email,
          defaultTeamMembership,
        } = this.form.values;
        await this.updateUser({
          firstName,
          lastName,
          email,
          profile: { defaultTeamMembership },
        });
        this.toast.success("User profile saved");
        this.form.fields.email.value = this.user.email;
        this.form.resetValidation();
      } catch (err) {
        if (err.response?.status === 400) {
          // Flatten nested profile fields
          if (
            Object.prototype.hasOwnProperty.call(err.response.data, "profile")
          ) {
            Object.entries(err.response.data.profile).forEach(
              ([key, value]) => {
                err.response.data[key] = value;
              }
            );
            delete err.response.data["profile"];
          }
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