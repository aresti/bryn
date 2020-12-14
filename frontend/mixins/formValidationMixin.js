export default {
  computed: {
    formIsValid() {
      return Object.values(this.form).every(
        (fieldObj) => fieldObj.valid || !fieldObj.validators?.length
      );
    },
    formValues() {
      return Object.entries(this.form).reduce((acc, [key, fieldObj]) => {
        acc[key] = fieldObj.value;
        return acc;
      }, {});
    },
  },
  methods: {
    validateForm() {
      Object.keys(this.form).forEach((key) => {
        this.validateField(key);
      });
    },
    validateField(name) {
      const field = this.form[name];
      field.errors = [];
      field.validators?.forEach((validator) => {
        try {
          validator(field.value);
        } catch (err) {
          field.errors.push(err);
        }
      });
      field.valid = !field.errors.length;
    },
    fieldIsInvalid(field) {
      return Boolean(field.errors?.length);
    },
  },
};
