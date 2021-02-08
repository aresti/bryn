import { createApp } from "vue";

import { axios } from "@/api";
import store from "@/store";
import router from "@/router";

import Toast, { POSITION } from "vue-toastification";
import VueClickAway from "vue3-click-away";

// Font Awesome
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faAngleDown,
  faBuilding,
  faCheck,
  faEye,
  faEyeSlash,
  faGlobeEurope,
  faHdd,
  faKey,
  faLink,
  faPhone,
  faPlusCircle,
  faSave,
  faServer,
  faSpinner,
  faTag,
  faTimes,
  faTrashAlt,
  faUniversity,
  faUnlink,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(
  faAngleDown,
  faBuilding,
  faCheck,
  faEye,
  faEyeSlash,
  faGlobeEurope,
  faHdd,
  faKey,
  faLink,
  faPhone,
  faPlusCircle,
  faSave,
  faServer,
  faSpinner,
  faTag,
  faTimes,
  faTrashAlt,
  faUniversity,
  faUnlink
);

// Create App
import App from "@/App";
const app = createApp(App);

// Plugin registration
app.use(store);
app.use(router);
app.config.globalProperties.$http = axios;
app.use(VueClickAway);
const toastOptions = {
  position: POSITION.BOTTOM_LEFT,
};
app.use(Toast, toastOptions);

// Global base component registration
app.component("font-awesome-icon", FontAwesomeIcon);

import BaseButton from "@/components/BaseButton";
import BaseButtons from "@/components/BaseButtons";
import BaseButtonCancel from "@/components/BaseButtonCancel";
import BaseButtonConfirm from "@/components/BaseButtonConfirm";
import BaseButtonCreate from "@/components/BaseButtonCreate";
import BaseButtonDelete from "@/components/BaseButtonDelete";
import BaseCard from "@/components/BaseCard";
import BaseDropdown from "@/components/BaseDropdown";
import BaseDropdownList from "@/components/BaseDropdownList";
import BaseFlexCentered from "@/components/BaseFlexCentered";
import BaseFormControl from "@/components/BaseFormControl";
import BaseFormField from "@/components/BaseFormField";
import BaseFormInput from "@/components/BaseFormInput";
import BaseFormInputSelect from "@/components/BaseFormInputSelect";
import BaseFormValidated from "@/components/BaseFormValidated";
import BaseFormValidatedControl from "@/components/BaseFormValidatedControl";
import BaseFormValidatedInput from "@/components/BaseFormValidatedInput";
import BaseHeroFull from "@/components/BaseHeroFull";
import BaseIcon from "@/components/BaseIcon";
import BaseLevel from "@/components/BaseLevel";
import BaseLevelItem from "@/components/BaseLevelItem";
import BaseMessage from "@/components/BaseMessage";
import BaseMiniLoader from "@/components/BaseMiniLoader";
import BaseModal from "@/components/BaseModal";
import BaseModalCardClassic from "@/components/BaseModalCardClassic";
import BaseModalDelete from "@/components/BaseModalDelete";
import BaseModalSplit from "@/components/BaseModalSplit";
import BaseNotification from "@/components/BaseNotification";
import BaseProgress from "@/components/BaseProgress";
import BaseTable from "@/components/BaseTable";
import BaseTag from "@/components/BaseTag";
import BaseTagControl from "@/components/BaseTagControl";
import BaseTabs from "@/components/BaseTabs";

app.component("BaseButton", BaseButton);
app.component("BaseButtons", BaseButtons);
app.component("BaseButtonCancel", BaseButtonCancel);
app.component("BaseButtonConfirm", BaseButtonConfirm);
app.component("BaseButtonCreate", BaseButtonCreate);
app.component("BaseButtonDelete", BaseButtonDelete);
app.component("BaseCard", BaseCard);
app.component("BaseDropdown", BaseDropdown);
app.component("BaseDropdownList", BaseDropdownList);
app.component("BaseFlexCentered", BaseFlexCentered);
app.component("BaseFormControl", BaseFormControl);
app.component("BaseFormField", BaseFormField);
app.component("BaseFormInput", BaseFormInput);
app.component("BaseFormInputSelect", BaseFormInputSelect);
app.component("BaseFormValidated", BaseFormValidated);
app.component("BaseFormValidatedControl", BaseFormValidatedControl);
app.component("BaseFormValidatedInput", BaseFormValidatedInput);
app.component("BaseHeroFull", BaseHeroFull);
app.component("BaseIcon", BaseIcon);
app.component("BaseLevel", BaseLevel);
app.component("BaseLevelItem", BaseLevelItem);
app.component("BaseMessage", BaseMessage);
app.component("BaseMiniLoader", BaseMiniLoader);
app.component("BaseModal", BaseModal);
app.component("BaseModalCardClassic", BaseModalCardClassic);
app.component("BaseModalDelete", BaseModalDelete);
app.component("BaseModalSplit", BaseModalSplit);
app.component("BaseNotification", BaseNotification);
app.component("BaseProgress", BaseProgress);
app.component("BaseTable", BaseTable);
app.component("BaseTag", BaseTag);
app.component("BaseTagControl", BaseTagControl);
app.component("BaseTabs", BaseTabs);

app.mount("#app");
