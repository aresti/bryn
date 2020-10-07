<template>
  <li class="list-group-item">
    {{ member.user.first_name }} {{ member.user.last_name }}
  </li>
</template>

<script>
export default {
  props: {
    member: {
      required: true,
      type: Object,
    },
  },
};
</script>
