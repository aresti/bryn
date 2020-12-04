<template>
  <Form @submit="onSubmit" v-slot="{ errors }" ref="instanceForm">
    <base-modal-card @closeModal="closeModal">
      <template v-slot:header>Launch new server</template>

      <template v-slot:default>
        <base-form-control label="Region" :error="errors.tenant">
          <div class="select is-fullwidth">
            <Field
              name="tenant"
              v-slot="{ field, handleChange }"
              :class="{ 'is-danger': errors.tenant }"
              :rules="tenantValidator"
            >
              <select
                v-bind="field"
                @change="onTenantSelect($event, handleChange)"
              >
                <option disable value="">Select a region</option>
                <tenant-select-option
                  v-for="tenant in tenants"
                  :key="tenant.id"
                  :tenant="tenant"
                />
              </select>
            </Field>
          </div>
        </base-form-control>

        <fieldset :disabled="selectedTenant == null">
          <base-form-control label="Flavor" :error="errors.flavor">
            <div
              class="select is-fullwidth"
              :class="{ 'is-danger': errors.flavor }"
            >
              <Field as="select" name="flavor" :rules="flavorValidator">
                <option disabled value="">Select a flavor</option>
                <option
                  v-for="flavor in flavors"
                  :key="flavor.id"
                  :value="flavor.id"
                >
                  {{ flavor.name }}
                </option>
              </Field>
            </div>
          </base-form-control>

          <base-form-control label="Image" :error="errors.image">
            <div
              class="select is-fullwidth"
              :class="{ 'is-danger': errors.image }"
            >
              <Field as="select" name="image">
                <option disabled value="">Select an image</option>
                <option
                  v-for="image in images"
                  :key="image.id"
                  :value="image.id"
                >
                  {{ image.name }}
                </option>
              </Field>
            </div>
          </base-form-control>

          <base-form-control label="Server name" :error="errors.name">
            <Field
              as="input"
              name="name"
              class="input"
              :class="{ 'is-danger': errors.name }"
              placeholder="e.g, my-server"
              :rules="nameValidator"
            />
          </base-form-control>
        </fieldset>
      </template>

      <template v-slot:footer>
        <base-button type="submit" color="success">Launch</base-button>
        <base-button-cancel @click="closeModal" />
      </template>
    </base-modal-card>
  </Form>
</template>

<script>
import BaseButton from "@/components/BaseButton";
import BaseButtonCancel from "@/components/BaseButtonCancel";
import BaseFormControl from "@/components/BaseFormControl";
import BaseModalCard from "@/components/BaseModalCard";
import TenantSelectOption from "@/components/TenantSelectOption.vue";

import { Field, Form } from "vee-validate";
import { mapState, mapGetters } from "vuex";
import * as yup from "yup";

// Custom messages for yup-based field validations
yup.setLocale({
  mixed: {
    oneOf: "Please select a value",
  },
});

export default {
  emits: {
    "close-modal": null,
  },

  components: {
    BaseButton,
    BaseButtonCancel,
    BaseFormControl,
    BaseModalCard,
    Form,
    Field,
    TenantSelectOption,
  },

  data() {
    return {
      selectedTenantId: null,
      nameValidator: yup
        .string()
        .required()
        .matches(/([a-zA-Z0-9\-]{3,})$/, {
          message:
            "Minimum 3 characters; only letters, numbers and hyphens allowed.",
        }),
    };
  },

  computed: {
    ...mapGetters(["tenants", "getTenantById"]),
    ...mapGetters("flavors", ["getFlavorsForTenant"]),
    ...mapGetters("images", ["getImagesForTenant"]),
    ...mapGetters("sshkeys", ["getSshKeysForTenant"]),
    selectedTenant() {
      return this.getTenantById(this.selectedTenantId);
    },
    images() {
      return this.selectedTenantId == null
        ? []
        : this.getImagesForTenant(this.selectedTenant);
    },
    flavors() {
      return this.selectedTenantId == null
        ? []
        : this.getFlavorsForTenant(this.selectedTenant);
    },
    sshkeys() {
      return this.selectedTenantId == null
        ? []
        : this.getSshKeysForTenant(this.selectedTenant);
    },
  },

  methods: {
    closeModal() {
      this.$emit("close-modal");
    },
    onSubmit(values) {
      console.log(JSON.stringify(values));
    },
    onTenantSelect(event, handleChange) {
      // Intercept change event and grab selected value
      const value = event.target.value;
      this.selectedTenantId =
        value && value.trim() ? parseInt(event.target.value) : null;

      // Call vee-validate handler to continue validation
      handleChange(event);
    },
    selectValidator(validObjects, value) {
      // Is the selected item a member of the relevant collection?
      if (validObjects.map((obj) => obj.id.toString()).includes(value)) {
        return true;
      }

      return "Please make a selection";
    },
    dependentSelectValidator(validObjects, value) {
      /**
       * For validations dependent on the selected tenant.
       * Don't validate until a tenant has been selected.
       */
      if (!this.selectedTenantId) {
        return true;
      }
      return this.selectValidator(validObjects, value);
    },
    tenantValidator(value) {
      return this.selectValidator(this.tenants, value);
    },
    flavorValidator(value) {
      return this.dependentSelectValidator(this.flavors, value);
    },
    imageValidator(value) {
      return this.dependentSelectValidator(this.iamges, value);
    },
  },

  watch: {
    selectedTenantId() {
      // Clear flavor and image selections on tenant change
      this.$refs.instanceForm.setValues({
        flavor: "",
        image: "",
      });
    },
  },
};
</script>