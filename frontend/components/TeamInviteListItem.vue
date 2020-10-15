<template>
  <li class="list-group-item d-flex align-items-center">
    <span class="py-1">{{ invite.email }}</span>
  </li>
</template>

<script>
export default {
  props: {
    invite: {
      required: true,
      type: Object,
    },
  },
};
</script>
