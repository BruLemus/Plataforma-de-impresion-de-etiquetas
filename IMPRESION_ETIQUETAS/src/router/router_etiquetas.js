import { createRouter, createWebHistory } from "vue-router";
import login from "../components/login.vue";
import comp_etiquetas from "../components/comp_etiquetas.vue";
import comp_tarima from "../components/comp_tarima.vue";
import comp_historial from "../components/comp_historial.vue";
import comp_inf from "../components/comp_inf.vue";
import comp_registro from "../components/comp_registro.vue";



const routes = [
  { path: "/", name: "login", component: login },
  { path: "/etiquetas", name: "comp_etiquetas", component: comp_etiquetas },
  { path: "/tarima", name: "comp_tarima", component: comp_tarima },
  { path: "/historial", name: "comp_historial", component: comp_historial },
  { path: "/inf", name: "comp_inf", component: comp_inf},
  { path: "/registro", name: "registro", component: comp_registro }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
