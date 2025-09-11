<!-- src/components/CompEtiquetas.vue -->
<template>
  <div class="app-container">
    <!-- Barra superior -->
    <header class="header" v-if="username">
      <div class="header-content">
        <h1 class="logo">📦 Generador de Etiquetas</h1>
        <div class="user-info">
          {{ username }} |
            <!-- Mesa --> <strong>{{ selectedMesa }}</strong> |
          Entrada: <strong>{{ horaEntrada }}</strong>
          <button class="btn-logout" @click="logout">Salir</button>
        </div>
      </div>
    </header>

    <!-- Layout con barra lateral -->
    <div class="layout">
      <!-- Barra lateral -->
      <aside class="sidebar" v-if="username">
        <nav class="menu">
          <ul>
            <li :class="{active: currentView === 'caja'}" @click="setView('caja')">Etiquetas por Caja</li>
            <li :class="{active: currentView === 'tarima'}" @click="setView('tarima')">Etiquetas por Tarima</li>
            <li :class="{active: currentView === 'historial'}" @click="setView('historial')">Historial</li>
            <li :class="{active: currentView === 'info'}" @click="setView('info')">Programador / Info</li>
          </ul>
        </nav>
      </aside>

      <!-- Contenido principal -->
      <main class="content">
        <!-- Login -->
        <div v-if="!username" class="login-card">
          <h2>Iniciar Sesión</h2>
          <input v-model="loginUser" type="text" placeholder="Usuario" class="login-input" />
          <select v-model="selectedMesa" class="login-input">
            <option disabled value="">Selecciona una mesa</option>
            <option v-for="mesa in mesas" :key="mesa" :value="mesa">{{ mesa }}</option>
          </select>
          <button class="btn-login" @click="login">Entrar</button>
        </div>

        <!-- Vista dinámica -->
        <div v-else>
          <section v-if="currentView === 'caja'">
            <h2>Etiquetas por Caja</h2>
            <p>Aquí va la lógica para generar etiquetas por caja.</p>
          </section>

          <section v-if="currentView === 'tarima'">
            <h2>Etiquetas por Tarima</h2>
            <p>Aquí va la lógica para generar etiquetas por tarima.</p>
          </section>

          <section v-if="currentView === 'historial'">
            <h2>Historial</h2>
            <p>Aquí se mostrarán las etiquetas generadas previamente.</p>
          </section>

          <section v-if="currentView === 'info'">
            <h2>Programador / Info</h2>
            <p>Desarrollado por Bruno Lemus González - Proyecto de Gestión de Etiquetas.</p>
          </section>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: null,
      loginUser: "",
      mesas: ["Mesa 1", "Mesa 2", "Mesa 3", "Mesa 4"],
      selectedMesa: "",
      horaEntrada: "",
      currentView: "caja" // vista por defecto
    };
  },
  methods: {
    login() {
      if (this.loginUser && this.selectedMesa) {
        this.username = this.loginUser;
        this.horaEntrada = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      } else {
        alert("Ingresa usuario y selecciona una mesa.");
      }
    },
    logout() {
      this.username = null;
      this.loginUser = "";
      this.selectedMesa = "";
      this.horaEntrada = "";
    },
    setView(view) {
      this.currentView = view;
    }
  }
};
</script>

<style scoped>
/* ==== LAYOUT GENERAL ==== */
.app-container {
  min-height: 100vh;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
}

.layout {
  display: flex;
  flex: 1;
  margin-top: 60px; /* altura de la barra superior */
}

/* ==== BARRA SUPERIOR ==== */
.header {
  background: linear-gradient(to right, #1e3a8a, #3b82f6);
  color: white;
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.header-content {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
}
.logo { font-size: 1.2rem; font-weight: bold; }
.user-info { font-weight: bold; font-size: 0.95rem; color: white; display: flex; align-items: center; gap: 10px; }
.btn-logout {
  background: #dc2626; color: white;
  border: none; padding: 4px 10px;
  border-radius: 6px; cursor: pointer;
}

/* ==== SIDEBAR ==== */
.sidebar {
  width: 220px;
  background: #1e293b;
  color: white;
  padding-top: 20px;
  min-height: calc(100vh - 60px);
}
.menu ul { list-style: none; padding: 0; margin: 0; }
.menu li {
  padding: 12px 20px;
  cursor: pointer;
  font-weight: 500;
  border-left: 4px solid transparent;
}
.menu li:hover {
  background: #334155;
}
.menu li.active {
  background: #3b82f6;
  border-left: 4px solid #facc15;
}

/* ==== CONTENIDO ==== */
.content {
  flex: 1;
  padding: 20px;
  background: #f9fafb;
}

/* ==== LOGIN ==== */
.login-card {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  background: white;
  text-align: center;
}
.login-input {
  width: 80%;
  padding: 8px;
  margin-bottom: 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.btn-login {
  background: #2563eb;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
</style>
