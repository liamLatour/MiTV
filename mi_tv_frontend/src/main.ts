import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VueCookies from "vue-cookies";
import withUUID from "vue-uuid";
import LazyLoadDirective from "./directives/LazyLoadDirective";
import VueScrollTo from "vue-scrollto";

// var ExifImage = require('exif').ExifImage;

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
  faFilm,
  faPause,
  faVolumeLow,
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
  faRightFromBracket,
  faFilm,
  faPause,
  faVolumeLow
);

const app = withUUID(createApp(App));
app.use(router);
app.use(VueScrollTo);
app.use(VueCookies, { expire: "1d" });
app.directive("lazyload", LazyLoadDirective);
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");
