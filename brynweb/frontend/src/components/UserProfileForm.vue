<template>
  <div>
    <h2>User Profile</h2>

    <div class="box">
      <base-form-validated
        :form="form"
        @fieldValidate="form.onFieldValidate"
        submitLabel="Update"
        @submit="alert('submit')"
        :submitted="submitted"
        requireInput
      />
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { isRequired } from "@/composables/formValidation/validators";
import useFormValidation from "@/composables/formValidation";

export default {
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
  mounted() {
    this.form.fields.firstName.value = this.user.firstName;
    this.form.fields.lastName.value = this.user.lastName;
    this.form.fields.email.value = this.user.email;
  },
};
</script>