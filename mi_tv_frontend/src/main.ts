import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VueCookies from "vue-cookies";

import LazyLoadDirective from "./directives/LazyLoadDirective";

import "./assets/main.css";

/* import fontawesome */
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faFolder,
  faDownload,
  faTimes,
  faPlay,
  faSpinner,
  faUpload,
  faBars,
  faUserGear,
  faGear,
  faRightFromBracket,
  faPen,
  faCheck,
} from "@fortawesome/free-solid-svg-icons";

library.add(
  faFolder,
  faDownload,
  faTimes,
  faPlay,
  faSpinner,
  faUpload,
  faBars,
  faUserGear,
  faGear,
  faPen,
  faCheck,
  faRightFromBracket
);

const app = createApp(App);
app.use(router);
app.use(VueCookies, { expire: "7d" });
app.directive("lazyload", LazyLoadDirective);
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");
