<template>
  <Form @submit="onSubmit" v-slot="{ errors }" ref="instanceForm">
    <base-modal-card-classic @closeModal="closeModal">
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
                <option disabled value="">Select a region</option>
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
              <Field as="select" name="image" :rules="imageValidator">
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

          <base-form-control label="SSH Key" :error="errors.keypair">
            <div
              class="select is-fullwidth"
              :class="{ 'is-danger': errors.keypair }"
            >
              <Field as="select" name="keypair" :rules="keypairValidator">
                <option disabled value="">Select a key</option>
                <option
                  v-for="keypair in keypairs"
                  :key="keypair.id"
                  :value="keypair.id"
                >
                  {{ keypair.name }}
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
    </base-modal-card-classic>
  </Form>
</template>

<script>
import BaseButton from "@/components/BaseButton";
import BaseButtonCancel from "@/components/BaseButtonCancel";
import BaseFormControl from "@/components/BaseFormControl";
import BaseModalCardClassic from "@/components/BaseModalCardClassic";
import TenantSelectOption from "@/components/TenantSelectOption";

import { mapActions, mapState, mapGetters } from "vuex";

export default {
  emits: {
    "close-modal": null,
  },

  components: {
    BaseButton,
    BaseButtonCancel,
    BaseFormControl,
    BaseModalCardClassic,
    Form,
    Field,
    TenantSelectOption,
  },

  data() {
    return {
      selectedTenantId: null,
    };
  },

  computed: {
    ...mapGetters(["tenants", "getTenantById"]),
    ...mapGetters("flavors", ["getFlavorsForTenant"]),
    ...mapGetters("images", ["getImagesForTenant"]),
    ...mapGetters("keypairs", ["getKeyPairsForTenant"]),
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
    keypairs() {
      return this.selectedTenantId == null
        ? []
        : this.getKeyPairsForTenant(this.selectedTenant);
    },
  },

  methods: {
    ...mapActions("instances", ["createInstance"]),
    closeModal() {
      this.$emit("close-modal");
    },
    async onSubmit(values) {
      try {
        const result = await this.createInstance(values);
        console.log(result);
      } catch (err) {
        console.log(err.response.data.detail);
      }
    },
    onTenantSelect(event, handleChange) {
      return;
    },
    selectValidator(validObjects, value) {
      // Is the selected item a member of the relevant collection?
      if (
        value != null &&
        validObjects.map((obj) => obj.id.toString()).includes(value)
      ) {
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
      return this.dependentSelectValidator(this.images, value);
    },
    keypairValidator(value) {
      return this.dependentSelectValidator(this.keypairs, value);
    },
  },

  watch: {
    selectedTenantId() {
      // Clear flavor and image selections on tenant change
      this.$refs.instanceForm.setValues({
        flavor: "",
        image: "",
        keypair: "",
      });
    },
  },
};
</script>