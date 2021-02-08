<template>
  <h2>User Profile</h2>

  <base-form-validated
    :form="form"
    submitLabel="Update"
    @submit="alert('submit')"
    :submitted="submitted"
    requireInput
  />
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
    ...mapState(["user"]),
  },
  mounted() {
    this.form.fields.firstName.value = this.user.firstName;
    this.form.fields.lastName.value = this.user.lastName;
    this.form.fields.email.value = this.user.email;
  },
};
</script>