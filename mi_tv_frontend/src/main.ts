import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import LazyLoadDirective from "./directives/LazyLoadDirective";

import "./assets/main.css";

/* import fontawesome */
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faFolder,
  faDownload,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";

library.add(faFolder, faDownload, faTimes);

const app = createApp(App);
app.use(router);
app.directive("lazyload", LazyLoadDirective);
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");
