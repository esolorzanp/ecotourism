import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/Login.vue";
import MainMenu from "../components/MainMenu.vue";

// -------------------------------------------- Componentes
// Componentes Usuarios
import UsuariosCreate from "../components/Usuarios/Usuarios-create.vue";
import UsuariosList from "../components/Usuarios/Usuarios-list.vue";
import UsuariosUpdate from "../components/Usuarios/Usuarios-update.vue";
// Componentes Sitios
import SitiosList from "../components/Sitios/Sitios-list.vue";
import SitiosCreate from "../components/Sitios/Sitios-create.vue";
import SitiosUpdate from "../components/Sitios/Sitios-update.vue";
// Componentes Comentarios
import ComentariosList from "../components/Comentarios/Comentarios-list.vue";
import ComentariosCreate from "../components/Comentarios/Comentarios-create.vue";
// Componentes Equipo
import EquipoList from "../components/Equipo/Equipo-list.vue";
import EquipoCreate from "../components/Equipo/Equipo-create.vue";
import EquipoUpdate from "../components/Equipo/Equipo-update.vue";
// Componentes PreguntasFrecuentes
import PreguntasFrecuentesList from "../components/PreguntasFrecuentes/PreguntasFrecuentes-list.vue";
import PreguntasFrecuentesCreate from "../components/PreguntasFrecuentes/PreguntasFrecuentes-create.vue";
import PreguntasFrecuentesUpdate from "../components/PreguntasFrecuentes/PreguntasFrecuentes-update.vue";

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
      path: "/usuarios-update/:id",
      name: "UsuariosUpdate",
      component: UsuariosUpdate,
    },
    {
      path: "/sitios-list",
      name: "SitiosList",
      component: SitiosList,
    },
    {
      path: "/sitios-create",
      name: "SitiosCreate",
      component: SitiosCreate,
    },
    {
      path: "/sitios-update/:id",
      name: "SitiosUpdate",
      component: SitiosUpdate,
    },
    {
      path: "/comentarios-list",
      name: "ComentariosList",
      component: ComentariosList,
    },
    {
      path: "/comentarios-create",
      name: "ComentariosCreate",
      component: ComentariosCreate,
    },
    {
      path: "/equipo-list",
      name: "EquipoList",
      component: EquipoList,
    },
    {
      path: "/equipo-create",
      name: "EquipoCreate",
      component: EquipoCreate,
    },
    {
      path: "/equipo-update/:id",
      name: "EquipoUpdate",
      component: EquipoUpdate,
    },
    {
      path: "/preguntasFrecuentes-list",
      name: "PreguntasFrecuentesList",
      component: PreguntasFrecuentesList,
    },
    {
      path: "/preguntasFrecuentes-create",
      name: "PreguntasFrecuentesCreate",
      component: PreguntasFrecuentesCreate,
    },
    {
      path: "/preguntasFrecuentes-update/:id",
      name: "PreguntasFrecuentesUpdate",
      component: PreguntasFrecuentesUpdate,
    },
  ],
});

export default router;
