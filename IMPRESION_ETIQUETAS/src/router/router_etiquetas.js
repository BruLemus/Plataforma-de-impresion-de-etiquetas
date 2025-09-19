import { createRouter, createWebHistory } from "vue-router";
import login from "../components/login.vue";
import comp_tarima from "../components/comp_tarima.vue";
import comp_historial from "../components/comp_historial.vue";
import comp_inf from "../components/comp_inf.vue";
import comp_registro from "../components/comp_registro.vue";

// Dashboards
import comp_etiquetas from "../components/comp_etiquetas.vue"; // Practicante
import CoordinadorDashboard from "../components/comp_inf.vue"; // Coordinador, usa tu componente real si es otro

const routes = [
  { path: "/", name: "login", component: login },
  { path: "/tarima", name: "comp_tarima", component: comp_tarima },
  { path: "/historial", name: "comp_historial", component: comp_historial },
  { path: "/inf", name: "comp_inf", component: comp_inf },
  { path: "/registro", name: "registro", component: comp_registro },

  // Dashboard Practicante
  {
    path: "/practicante",
    name: "dashboard_practicante",
    component: comp_etiquetas,
  },

  // Dashboard Coordinador
  {
    path: "/coordinador",
    name: "dashboard_coordinador",
    component: CoordinadorDashboard,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Protección de rutas opcional
router.beforeEach((to, from, next) => {
  const rol = localStorage.getItem("rol");

  if (to.name === "dashboard_practicante" && rol !== "Practicante") {
    next("/"); // Solo practicantes
  } else if (to.name === "dashboard_coordinador" && rol !== "Coordinador") {
    next("/"); // Solo coordinadores
  } else {
    next();
  }
});

export default router;
