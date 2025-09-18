<template>
  <div id="app" class="flex min-h-screen">
    <!-- Contenido principal -->
    <main class="flex-1 bg-gray-50">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem("username");
    },
  },
};
</script>

<style>
.sidebar {
  width: 220px;
  background: #1f2937;
  color: white;
  padding: 20px;
}
.sidebar a {
  display: block;
  padding: 10px;
  color: #d1d5db;
  text-decoration: none;
}
.sidebar a.router-link-active {
  background: #374151;
  border-radius: 6px;
}
</style>
