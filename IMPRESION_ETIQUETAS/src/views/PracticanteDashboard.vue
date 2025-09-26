<template>
  <div class="dashboard-wrapper">
    <h1>Dashboard Practicante</h1>

    <!-- 🔹 Enlaces a las vistas hijas -->
    <div class="dashboard-nav">
      <router-link :to="{ name: 'CompEtiquetas' }">Etiquetas</router-link>
    </div>

    <!-- 🔹 Aquí se cargará CompEtiquetas.vue -->
    <div class="dashboard-content">
      <router-view></router-view>
    </div>
  </div>
</template>
