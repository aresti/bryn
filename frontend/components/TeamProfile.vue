<template>
  <base-form-validated
    :form="form"
    submitLabel="Update"
    @submit="onSubmit"
    :submitted="submitted"
    :nonFieldErrors="nonFieldErrors"
    :disabled="!userIsAdmin"
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
          iconClasses: ["fas", "fa-university"],
        },
        department: {
          value: "",
          iconClasses: ["fas", "fa-building"],
        },
        phoneNumber: {
          label: "Phone",
          value: "",
          iconClasses: ["fas", "fa-phone"],
          validators: [isRequired],
        },
      },
      nonFieldErrors: [],
      submitted: false,
    };
  },

  computed: {
    ...mapGetters(["team", "userIsAdmin"]),
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

  watch: {
    team: {
      handler(_new, _old) {
        this.form.institution.value = this.team.institution;
        this.form.department.value = this.team.department;
        this.form.phoneNumber.value = this.team.phoneNumber;
      },
      immediate: true,
    },
  },
};
</script>