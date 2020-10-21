<template>
  <tr>
    <td :colspan="7">
      <base-progress color="primary" size="large" value="false" class="mt-3" />
    </td>
  </tr>
</template>

<script>
import BaseProgress from "./BaseProgress.vue";

export default {
  components: { BaseProgress },
};
</script>