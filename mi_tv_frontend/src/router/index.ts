import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/photos/:path(.*)*",
      name: "photos",
      component: () => import("../views/GalleryView.vue"),
    },
    {
      path: "/mes_photos/:path(.*)*",
      name: "mes_photos",
      component: () => import("../views/GalleryView.vue"),
      props: {
        url: "",
        isGlobal: false,
      },
    },
    {
      path: "/upload",
      name: "upload",
      component: () => import("../views/UploadView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/AdminLoginView.vue"),
    },
  ],
});

export default router;
