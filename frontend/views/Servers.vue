<template>
  <main>
    <template v-if="erroredOnGet">
      <base-message color="danger" dismissable>
        An error occurred while trying to get your servers. Your tenant(s) may
        be temporarily unavailable.
      </base-message>
    </template>
    <template v-else>
      <div class="container mb-3">
        <base-level>
          <template v-slot:left>
            <base-level-item>
              <base-button-create @click="showLaunchInstanceModal = true"
                >New server</base-button-create
              >
            </base-level-item>
          </template>
          <template v-slot:right>
            <base-level-item v-if="hasShelved">
              <base-button
                rounded
                :size="size"
                @click="showShelved = !showShelved"
                ><template v-slot:icon-before>
                  <base-icon
                    :size="size"
                    :fa-classes="[
                      'fas',
                      showShelved ? 'fa-eye-slash' : 'fa-eye',
                    ]"
                    :decorative="true"
                  />
                </template>
                <template v-slot:default>{{
                  showShelved ? "Hide shelved" : "Show shelved"
                }}</template>
              </base-button>
            </base-level-item>
          </template>
        </base-level>
      </div>
      <instance-table :instances="instances" :loading="loading" />
    </template>

    <launch-instance-modal
      v-if="showLaunchInstanceModal"
      @close-modal="showLaunchInstanceModal = false"
    />
  </main>
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
    InstanceTable,
    LaunchInstanceModal,
  },
  data() {
    return {
      showShelved: false,
      showLaunchInstanceModal: false,
    };
  },
  computed: {
    ...mapState("instances", {
      loading: (state) => state.loading,
      erroredOnGet: (state) => state.erroredOnGet,
    }),
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