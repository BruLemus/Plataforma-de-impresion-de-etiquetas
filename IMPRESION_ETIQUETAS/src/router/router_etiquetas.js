// src/router/router_etiquetas.js
import { createRouter, createWebHistory } from "vue-router";
import ViewsLogin from "@/views/views_login.vue";
import ViewsEtiquetas from "@/views/views_etiquetas.vue";


const routes = [
  {
    path: "/",
    name: "Login",
    component: ViewsLogin,
  },
  {
    path: "/etiquetas",
    name: "Etiquetas",
    component: ViewsEtiquetas,
   beforeEnter: (to, from, next) => {
  const username = localStorage.getItem("username");
  if (!username) {
    next("/"); // redirige al login si no hay usuario
  } else {
    next();
  }
}

  }, 
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;