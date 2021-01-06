<template>
  <h2>Team: {{ team.name }}</h2>

  <base-form-validated
    :form="form"
    submitLabel="Update"
    @submit="onSubmit"
    :submitted="submitted"
    requireInput
  />
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { isRequired } from "@/utils/validators";
import { useToast } from "vue-toastification";
import formValidationMixin from "@/mixins/formValidationMixin";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

  mixins: [formValidationMixin],

  data() {
    return {
      form: {
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
      submitted: false,
    };
  },

  computed: {
    ...mapGetters(["team"]),
  },

  methods: {
    ...mapActions(["updateTeam"]),
    async onSubmit() {
      this.formValidate();
      if (this.submitted || !this.formIsValid) {
        return;
      }
      this.submitted = true;
      try {
        await this.updateTeam(this.formValues);
        this.toast.success("Team profile saved");
        this.formResetValidation();
      } catch (err) {
        if (err.response?.status === 400) {
          this.formParseResponseError(err.response.data);
        } else {
          this.toast.error(
            `Failed to update team: ${
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
    this.form.institution.value = this.team.institution;
    this.form.department.value = this.team.department;
    this.form.phoneNumber.value = this.team.phoneNumber;
  },
};
</script>