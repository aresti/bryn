<template>
  <li class="list-group-item d-flex align-items-center">
    <span class="py-1"
      >{{ member.user.first_name }} {{ member.user.last_name }}</span
    >
    <span v-if="member.is_admin" class="badge badge-pill badge-success ml-auto"
      >Team Admin</span
    >
    <delete-button v-else class="ml-auto btn-sm" @click="deleteMember"
      >Remove</delete-button
    >
  </li>
</template>

<script>
import DeleteButton from "./DeleteButton.vue";

export default {
  emits: {
    "delete-member": null,
  },
  components: {
    DeleteButton,
  },
  props: {
    member: {
      required: true,
      type: Object,
    },
  },
  data() {
    return {
      showDeleteModal: true,
    };
  },
  methods: {
    deleteMember() {
      this.$emit("delete-member");
    },
  },
};
</script>
