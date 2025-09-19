<template>
  <div class="dashboard-wrapper">
    <h1>Dashboard Coordinador</h1>
    
    <nav class="dashboard-nav">
      <router-link :to="{ name: 'comp_etiquetas' }">Etiquetas</router-link>
      <router-link :to="{ name: 'comp_tarima' }">Tarimas</router-link>
      <router-link :to="{ name: 'comp_historial' }">Historial</router-link>
    </nav>

    <div class="dashboard-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: "CoordinadorDashboard"
};
</script>

<style scoped>
.dashboard-wrapper {
  padding: 20px;
}

.dashboard-nav {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.dashboard-nav a {
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 8px;
  background: #0fa8cb;
  color: white;
  font-weight: bold;
}

.dashboard-nav a.router-link-exact-active {
  background: #1e3a8a;
}

.dashboard-content {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 12px;
}
</style>
