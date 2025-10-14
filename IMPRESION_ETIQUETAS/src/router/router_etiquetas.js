import { createRouter, createWebHistory } from "vue-router";

// Componentes generales
import login from "../components/login.vue";
import comp_tarima from "../components/comp_tarima.vue";
import comp_historial from "../components/comp_historial.vue";
import comp_inf from "../components/comp_inf.vue";
import comp_registro_gdl from "../components/comp_registro_coordinadores.vue";
import crear_practicante_gdl from "../components/comp_crear_practicante.vue";
import comp_otras_etiquetas from "../components/comp_otras_etiquetas.vue";

// Dashboards GDL
import comp_etiquetas_practicantes from "../components/comp_etiquetas_practicantes.vue";
import comp_etiquetas_coordinador from "../components/comp_etiquetas_coordinador.vue";

// Componentes México
import Comp_tarima_mx from "../components/comp_tarima_mx.vue";
import Comp_historial_mx from "../components/comp_historial_mx.vue";
import comp_registro_coordinadores_mx from "../components/comp_registro_coordinadores_mx.vue";
import crear_practicante_mx from "../components/comp_crear_practicante_mx.vue";
import comp_practicantes_mx from "../components/comp_etiquetas_practicantes_mx.vue";
import comp_etiquetas_coordinador_mx from "../components/comp_etiquetas_coordinador_mx.vue";

const routes = [
  // Login
  { path: "/", name: "login", component: login },

  // Rutas GDL
  { path: "/tarima", name: "comp_tarima", component: comp_tarima, meta: { requiresAuth: true } },
  { path: "/historial", name: "comp_historial", component: comp_historial, meta: { requiresAuth: true } },
  { path: "/inf", name: "comp_inf", component: comp_inf, meta: { requiresAuth: true } },
  { path: "/registro", name: "registro_gdl", component: comp_registro_gdl },
  { path: "/crearpracticante", name: "crear_practicante_gdl", component: crear_practicante_gdl, meta: { requiresAuth: true } },
  { path: "/otrasetiquetas", name: "comp_otras_etiquetas", component: comp_otras_etiquetas, meta: { requiresAuth: true } },

  // Dashboards GDL
  { path: "/practicante", name: "dashboard_practicante", component: comp_etiquetas_practicantes, meta: { requiresAuth: true } },
  { path: "/coordinador", name: "dashboard_coordinadores", component: comp_etiquetas_coordinador, meta: { requiresAuth: true } },

  // Rutas México
  { path: "/tarima_mx", name: "comp_tarima_mx", component: Comp_tarima_mx, meta: { requiresAuth: true } },
  { path: "/historial_mx", name: "comp_historial_mx", component: Comp_historial_mx, meta: { requiresAuth: true } },
  { path: "/registro_mx", name: "registro_mx", component: comp_registro_coordinadores_mx },
  { path: "/crearpracticante_mx", name: "crear_practicante_mx", component: crear_practicante_mx, meta: { requiresAuth: true } },

  // Dashboards México
  { path: "/practicante_mx", name: "dashboard_practicante_mx", component: comp_practicantes_mx, meta: { requiresAuth: true } },
  { path: "/coordinador_mx", name: "dashboard_coordinadores_mx", component: comp_etiquetas_coordinador_mx, meta: { requiresAuth: true } },

  // Ruta dinámica según ciudad y tipo
  {
    path: "/:ciudad/:tipo",
    name: "dashboard_dynamic",
    component: { render() { return null; } }, // Componente vacío solo para redirección
    beforeEnter: (to, from, next) => {
      const ciudad = to.params.ciudad.toLowerCase();
      const tipo = to.params.tipo.toLowerCase();

      if (ciudad === "mx") {
        if (tipo === "practicante") return next({ name: "dashboard_practicante_mx" });
        if (tipo === "coordinador") return next({ name: "dashboard_coordinadores_mx" });
      } else {
        if (tipo === "practicante") return next({ name: "dashboard_practicante" });
        if (tipo === "coordinador") return next({ name: "dashboard_coordinadores" });
      }

      next("/otrasetiquetas"); // fallback
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Protección global de rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    alert("Debes iniciar sesión para acceder");
    return next("/");
  }

  next();
});

export default router;
