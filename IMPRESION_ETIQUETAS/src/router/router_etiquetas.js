import { createRouter, createWebHistory } from "vue-router";
import Views_etiquetas from "@/views/views_etiquetas.vue";

const routes = [
  {
    path: "/etiquetas",   // ruta principal
    name: "etiqueta",
    component: Views_etiquetas,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
