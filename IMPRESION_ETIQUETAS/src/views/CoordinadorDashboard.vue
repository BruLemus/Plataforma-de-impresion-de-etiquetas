<template>
  <div class="dashboard-wrapper">
    <h1>Dashboard Cordinadores</h1>

    <!-- 🔹 Enlaces a las vistas hijas -->
    <div class="dashboard-nav">
      <router-link :to="{ name: 'CompEtiquetas' }">Etiquetas</router-link>
    </div>

    <div class="dashboard-content">
      <router-view></router-view>
    </div>
  </div>
</template>
