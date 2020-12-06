<template>
  <div>
    <div class="container mb-3">
      <base-level>
        <template v-slot:left>
          <base-level-item>
            <base-tabs toggle rounded>
              <li :class="{ 'is-active': filterTenant == null }">
                <a @click="filterTenant = null">All</a>
              </li>
              <li
                v-for="tenant in tenants"
                :key="tenant.id"
                :class="{ 'is-active': tenant === filterTenant }"
              >
                <a @click="filterTenant = tenant">{{
                  getRegionNameForTenant(tenant)
                }}</a>
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
    <instance-table :instances="filteredInstances" />

    <launch-instance-modal
      v-if="showLaunchInstanceModal"
      @closeModal="showLaunchInstanceModal = false"
    />
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import { mapGetters, mapState } from "vuex";

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
    ...mapState("instances", ["all"]),
    ...mapGetters(["tenants", "getRegionNameForTenant"]),
    ...mapGetters("instances", ["notShelved"]),
    filteredInstances() {
      const byStatus = this.showShelved ? this.all : this.notShelved;
      if (this.filterTenant == null) {
        return byStatus;
      }
      return byStatus.filter(
        (instance) => instance.tenant === this.filterTenant.id
      );
    },
    hasShelved() {
      return this.all.length !== this.notShelved.length;
    },
  },
};
</script>