<template>
  <li class="list-group-item d-flex align-items-center">
    <span class="py-1"
      >{{ member.user.first_name }} {{ member.user.last_name }}</span
    >
    <span v-if="member.is_admin" class="badge badge-pill badge-success ml-auto"
      >Team Admin</span
    >
    <base-button
      v-else
      context="danger"
      class="ml-auto"
      is-outline
      is-small
      @click="deleteMember"
      >Remove</base-button
    >
  </li>
</template>

<script>
import BaseButton from "./BaseButton.vue";

export default {
  emits: {
    "delete-member": null,
  },
  components: {
    BaseButton,
  },
  props: {
    member: {
      required: true,
      type: Object,
    },
  },
  methods: {
    deleteMember() {
      this.$emit("delete-member");
    },
  },
};
</script>
