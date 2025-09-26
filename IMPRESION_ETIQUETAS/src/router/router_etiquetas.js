import { createRouter, createWebHistory } from "vue-router";
import login from "../components/login.vue";
import comp_tarima from "../components/comp_tarima.vue";
import comp_historial from "../components/comp_historial.vue";
import comp_inf from "../components/comp_inf.vue";
import comp_registro from "../components/comp_registro.vue";


// Dashboards
import comp_etiquetas_practicantes from "../components/comp_etiquetas_practicantes.vue"; //Practicantes 
import comp_etiquetas_coordinador from "../components/comp_etiquetas_coordinador.vue" //coordinadores
import comp_otras_etiquetas from "../components/comp_otras_etiquetas.vue"

const routes = [
  { path: "/", name: "login", component: login },
  { path: "/tarima", name: "comp_tarima", component: comp_tarima },
  { path: "/historial", name: "comp_historial", component: comp_historial },
  { path: "/inf", name: "comp_inf", component: comp_inf },
  { path: "/registro", name: "registro", component: comp_registro },
  { path: "/otrasetiquetas", name: "comp_otras_etiquetas", component: comp_otras_etiquetas},

  // Dashboard Practicante
  {
    path: "/practicante",
    name: "dashboard_practicante",
    component: comp_etiquetas_practicantes,
  },

  // Dashboard Coordinador
  {
    path: "/coordinador",
    name: "dashboard_coordinadores",
    component: comp_etiquetas_coordinador,
    meta: { requiresAuth: true }

  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Protección de rutas opcional
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Debes iniciar sesión para acceder");
      return next("/");
    }
  }
  next();
});

export default router;
