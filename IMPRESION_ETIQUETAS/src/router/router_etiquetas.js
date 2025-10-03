import { createRouter, createWebHistory } from "vue-router";
import login from "../components/login.vue";
import comp_tarima from "../components/comp_tarima.vue";
import comp_historial from "../components/comp_historial.vue";
import comp_inf from "../components/comp_inf.vue";
import comp_registro from "../components/comp_registro.vue";

// Dashboards
import comp_etiquetas_practicantes from "../components/comp_etiquetas_practicantes.vue";
import comp_etiquetas_coordinador from "../components/comp_etiquetas_coordinador.vue";
import comp_otras_etiquetas from "../components/comp_otras_etiquetas.vue";

const routes = [
  { path: "/", name: "login", component: login },
  { path: "/tarima", name: "comp_tarima", component: comp_tarima },
  { path: "/historial", name: "comp_historial", component: comp_historial, meta: { requiresAuth: true }},
  { path: "/inf", name: "comp_inf", component: comp_inf },
  { path: "/registro", name: "registro", component: comp_registro },
  { path: "/otrasetiquetas", name: "comp_otras_etiquetas", component: comp_otras_etiquetas },

  // Dashboards fijos
  {
    path: "/practicante",
    name: "dashboard_practicante",
    component: comp_etiquetas_practicantes,
  },
  {
    path: "/coordinador",
    name: "dashboard_coordinadores",
    component: comp_etiquetas_coordinador,
    meta: { requiresAuth: true }
  },

  // Ruta dinámica según ciudad y tipo
  {
    path: "/:ciudad/:tipo",
    name: "dashboard_dynamic",
    component: {
      render() { return null; } // Componente vacío, solo para redirección
    },
    beforeEnter: (to, from, next) => {
      const tipo = to.params.tipo.toLowerCase();
      if (tipo === "practicante") return next({ name: "dashboard_practicante" });
      if (tipo === "coordinador") return next({ name: "dashboard_coordinadores" });
      next("/otrasetiquetas"); // fallback
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Protección de rutas solo para coordinadores
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
