<template>
  <base-dropdown right :hoverable="hoverable">
    <template v-slot:trigger="{ toggle: toggleDropdown }">
      <base-button
        @click="toggleDropdown"
        rounded
        dropdown
        outlined
        color="white"
      >
        Switch team
      </base-button>
    </template>
    <template v-slot="{ toggle: toggleDropdown }">
      <a
        v-for="team in teams"
        :key="team.id"
        @click="
          toggleDropdown();
          selectTeam(team);
        "
        class="dropdown-item"
        :class="{
          'is-active': team == currentTeam,
          'has-text-weight-bold': team == currentTeam,
        }"
      >
        {{ team.name }}
      </a>
    </template>
  </base-dropdown>
</template>

<script>
import BaseButton from "./BaseButton.vue";
import BaseDropdown from "./BaseDropdown.vue";

export default {
  components: {
    BaseButton,
    BaseDropdown,
  },
  props: {
    teams: {
      type: Array,
      required: true,
    },
    currentTeam: {
      type: Object,
      required: true,
    },
    hoverable: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    selectTeam(team) {
      this.$emit("teamSelected", team);
    },
  },
  emits: {
    teamSelected: null,
  },
};
</script>