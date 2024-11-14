import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/Login.vue";
import MainMenu from "../components/MainMenu.vue";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/Login",
      name: "Login",
      component: Login,
    },
    {
      path: "/MainMenu",
      name: "MainMenu",
      component: MainMenu,
    },
  ],
});

export default router;
