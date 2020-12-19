<template>
  <h2>Team Profile</h2>

  <base-form-validated
    :form="form"
    submitLabel="Update"
    @validate-field="formValidate"
    @submit="onSubmit"
  />
</template>

<script>
import { mapGetters } from "vuex";
import { isRequired } from "@/utils/validators";
import formValidationMixin from "@/mixins/formValidationMixin";

export default {
  mixins: [formValidationMixin],
  data() {
    return {
      form: {
        name: {
          value: "",
          validators: [isRequired],
        },
        institution: {
          value: "",
          validators: [isRequired],
        },
        department: {
          value: "",
        },
        phoneNumber: {
          label: "Phone",
          value: "",
          validators: [isRequired],
        },
      },
    };
  },
  computed: {
    ...mapGetters(["team"]),
  },
  mounted() {
    this.form.name.value = this.team.name;
    this.form.institution.value = this.team.institution;
    this.form.department.value = this.team.department;
    this.form.phoneNumber.value = this.team.phoneNumber;
  },
};
</script>