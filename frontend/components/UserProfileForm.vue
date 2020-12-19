<template>
  <h2>User Profile</h2>

  <base-form-validated
    :form="form"
    submitLabel="Update"
    @validate-field="formValidate"
    @submit="onSubmit"
  />
</template>

<script>
import { mapState } from "vuex";
import { isRequired } from "@/utils/validators";
import formValidationMixin from "@/mixins/formValidationMixin";

export default {
  mixins: [formValidationMixin],
  data() {
    return {
      form: {
        firstName: {
          label: "First name",
          value: "",
          validators: [isRequired],
        },
        lastName: {
          label: "Last name",
          value: "",
          validators: [isRequired],
        },
        email: {
          label: "Email",
          value: "",
          validators: [isRequired],
        },
      },
    };
  },
  computed: {
    ...mapState(["user"]),
  },
  mounted() {
    this.form.firstName.value = this.user.firstName;
    this.form.lastName.value = this.user.lastName;
    this.form.email.value = this.user.email;
  },
};
</script>