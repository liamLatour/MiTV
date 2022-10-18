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
      path: "/mes_photos",
      name: "mes_photos",
      component: () => import("../views/GalleryView.vue"),
      props: {
        url: "/get_by_name/munier",
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
