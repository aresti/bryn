<template>
  <div>
    <div class="container mb-3">
      <base-level>
        <template v-slot:left>
          <base-level-item>
            <base-tabs class="is-toggle is-toggle-rounded">
              <li :class="{ 'is-active': filterTenant == null }"><a>All</a></li>
              <li
                v-for="tenant in tenants"
                :key="tenant.id"
                :class="{ 'is-active': tenant.id === filterTenant }"
              >
                <a>{{ getRegionNameForTenant(tenant) }}</a>
              </li>
            </base-tabs>
          </base-level-item>
        </template>
        <template v-slot:right>
          <base-level-item v-if="hasShelved">
            <base-button rounded @click="showShelved = !showShelved"
              ><template v-slot:icon-before>
                <base-icon
                  :fa-classes="[
                    'fas',
                    showShelved ? 'fas fa-eye-slash' : 'fas fa-eye',
                  ]"
                  :decorative="true"
                />
              </template>
              <template v-slot:default>{{
                showShelved ? "Hide shelved" : "Show shelved"
              }}</template>
            </base-button>
          </base-level-item>
          <base-level-item>
            <base-button-create @click="showLaunchInstanceModal = true">
              New server
            </base-button-create>
          </base-level-item>
        </template>
      </base-level>
    </div>
    <instance-table :instances="instances" />

    <launch-instance-modal
      v-if="showLaunchInstanceModal"
      @closeModal="showLaunchInstanceModal = false"
    />
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import { mapGetters } from "vuex";

import BaseButton from "@/components/BaseButton";
import BaseButtonCreate from "@/components/BaseButtonCreate";
import BaseIcon from "@/components/BaseIcon";
import BaseLevel from "@/components/BaseLevel";
import BaseLevelItem from "@/components/BaseLevelItem";
import BaseMessage from "@/components/BaseMessage";
import BaseTabs from "@/components/BaseTabs";
import LaunchInstanceModal from "@/components/LaunchInstanceModal";
import InstanceTable from "@/components/InstanceTable";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },
  components: {
    BaseButton,
    BaseButtonCreate,
    BaseIcon,
    BaseLevel,
    BaseLevelItem,
    BaseMessage,
    BaseTabs,
    InstanceTable,
    LaunchInstanceModal,
  },
  data() {
    return {
      filterTenant: null,
      showShelved: false,
      showLaunchInstanceModal: false,
    };
  },
  computed: {
    ...mapGetters(["tenants", "getRegionNameForTenant"]),
    ...mapGetters("instances", ["allFormatted", "notShelvedFormatted"]),
    instances() {
      if (this.showShelved) {
        return this.allFormatted;
      } else {
        return this.notShelvedFormatted;
      }
    },
    hasShelved() {
      return this.allFormatted.length !== this.notShelvedFormatted.length;
    },
  },
};
</script>