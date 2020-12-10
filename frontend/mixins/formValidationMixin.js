export default {
  computed: {
    formValid() {
      return Object.values(this.form).every(
        (fieldObj) => fieldObj.valid || !fieldObj.validators?.length
      );
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
