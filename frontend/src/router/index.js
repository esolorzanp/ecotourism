import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/Login.vue";
import MainMenu from "../components/MainMenu.vue";

// -------------------------------------------- Componentes 
// Componentes Usuarios
import UsuariosCreate from "../components/usuarios/Usuarios-create.vue"
import UsuariosList from "../components/usuarios/Usuarios-list.vue"
import UsuariosUpdate from "../components/usuarios/Usuario-update.vue";
// Componentes Sitios
import SitiosList from "../components/Sitios/Sitios-list.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/Login",
      name: "Login",
      component: Login,
    },
    {
      path: "/menu",
      name: "MainMenu",
      component: MainMenu,
    },
    {
      path: "/usuarios-list",
      name: "UsuariosList",
      component: UsuariosList,
    },
    {
      path: "/usuarios-create",
      name: "UsuariosCreate",
      component: UsuariosCreate,
    },
    {
      path: "/usuarios-update",
      name: "UsuariosUpdate",
      component: UsuariosUpdate,
    },
    {
      path: "/sitios",
      name: "SitiosList",
      component: SitiosList,
    },
  ],
});

export default router;
