<!-- src/components/comp_historial.vue -->
<template>
  <div class="app-container">
    <!-- BARRA SUPERIOR -->
    <header class="header">
      <div class="header-content">
        <h1 class="logo">📑 Historial de Etiquetas Generadas</h1>
        <div class="user-info">
          🚹 {{ username }} |
          <strong v-if="mesaSeleccionada">💻 Mesa de trabajo: {{ mesaSeleccionada }}</strong> |
          🕖 Entrada: <strong v-if="horaEntrada">{{ horaEntrada }}</strong>
          <button class="btn-logout" @click="logout">Salir</button>
        </div>
      </div>
    </header>

    <!-- CONTENIDO -->
    <main class="content">
      <div class="crud-card">
        <h2 class="crud-subtitle">Registros Generados</h2>

        <!-- FILTROS -->
        <div class="filters">
          <div class="search-box">
            <input
              type="text"
              v-model="busquedaFactura"
              placeholder="Buscar por factura..."
            />
            <span class="lupa">🔍</span>
          </div>

          <select v-model="filtroTipo">
            <option value="Todos">Todos</option>
            <option value="Cajas">Cajas</option>
            <option value="Tarimas">Tarimas</option>
          </select>
        </div>

        <!-- TABLA -->
        <table class="historial-table">
          <thead>
            <tr>
              <th>Usuario</th>
              <th>Hora de Inicio</th>
              <th>Factura</th>
              <th>Paquetería</th>
              <th>Cantidad</th>
              <th>Piezas</th>
              <th>Tipo de Embalaje</th>
              <th>Clave de Producto</th>
              <th>Tipo Registro</th>
              <th>Hora de Creación</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in historialFiltrado" :key="index">
              <td>{{ item.usuario }}</td>
              <td>{{ item.horaInicio }}</td>
              <td>{{ item.factura }}</td>
              <td>{{ item.paqueteria }}</td>
              <td>{{ item.cantidad }}</td>
              <td>{{ item.piezas }}</td>
              <td>{{ item.tipoEmbalaje }}</td>
              <td>{{ item.claveProducto }}</td>
              <td>
                <span
                  :class="item.tipoRegistro === 'Cajas' ? 'badge-caja' : 'badge-tarima'"
                >
                  {{ item.tipoRegistro }}
                </span>
              </td>
              <td>{{ item.horaCreacion }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "comp_historial",
  data() {
    return {
      username: localStorage.getItem("username") || "",
      mesaSeleccionada: localStorage.getItem("mesaSeleccionada") || "",
      horaEntrada: localStorage.getItem("horaEntrada") || "",
      busquedaFactura: "",
      filtroTipo: "Todos",
      historial: [
        {
          usuario: "Bruno Lemus",
          horaInicio: "2025-09-11 08:30",
          factura: "F00123",
          paqueteria: "DHL",
          cantidad: 5,
          piezas: 50,
          tipoEmbalaje: "Caja de cartón",
          claveProducto: "P-001",
          tipoRegistro: "Cajas",
          horaCreacion: "2025-09-11 08:45",
        },
        {
          usuario: "Ana Pérez",
          horaInicio: "2025-09-11 09:00",
          factura: "F00124",
          paqueteria: "FedEx",
          cantidad: 1,
          piezas: 300,
          tipoEmbalaje: "Tarima de madera",
          claveProducto: "P-002",
          tipoRegistro: "Tarimas",
          horaCreacion: "2025-09-11 09:10",
        },
      ],
    };
  },
  computed: {
    historialFiltrado() {
      return this.historial.filter((item) => {
        const coincideFactura = item.factura
          .toLowerCase()
          .includes(this.busquedaFactura.toLowerCase());

        const coincideTipo =
          this.filtroTipo === "Todos" || item.tipoRegistro === this.filtroTipo;

        return coincideFactura && coincideTipo;
      });
    },
  },
  methods: {
    logout() {
      localStorage.removeItem("username");
      localStorage.removeItem("mesaSeleccionada");
      localStorage.removeItem("horaEntrada");
      this.$router.push("/");
    },
  },
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

/* BARRA SUPERIOR */
.header { background: linear-gradient(to right, #131a2e, #4274c4); color: rgb(196, 205, 217); position: fixed; top: 0; left: 0; right: 0; z-index: 100; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }

.header-content {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
}
.logo {
  font-size: 1.2rem;
  font-weight: bold;
}
.user-info {
  font-weight: bold;
  font-size: 0.95rem;
  color: white;
  display: flex;
  align-items: center;
  gap: 10px;
}
.btn-logout {
  background: #c6c4c4;
  color: rgb(18, 6, 6);
  border: none;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
}

/* CONTENIDO */
.content {
  flex: 1;
  padding: 100px 20px 20px;
  background: #f9fafb;
}

/* TARJETA */
.crud-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  max-width: 1100px;
  margin: 20px auto;
  padding: 18px;
  border: 1px solid #e5e7eb;
}
.crud-subtitle {
  font-weight: 700;
  margin-bottom: 12px;
}

/* FILTROS */
.filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  gap: 10px;
  align-items: center;
}
.search-box {
  position: relative;
  width: 250px;
}
.search-box input {
  width: 100%;
  padding: 6px 28px 6px 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.search-box .lupa {
  position: absolute;
  right: 8px;
  top: 6px;
  font-size: 1rem;
}
select {
  padding: 6px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

/* TABLA */
.historial-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}
.historial-table th,
.historial-table td {
  border: 1px solid #ccc;
  padding: 10px;
}
.historial-table th {
  background-color: #051e5a;
  color: white;
  font-weight: bold;
}
.historial-table tr:nth-child(even) {
  background-color: #f2f2f2;
}
.historial-table tr:hover {
  background-color: #dbeafe;
}

/* BADGES */
.badge-caja {
  background: #16a34a;
  color: white;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: bold;
}
.badge-tarima {
  background: #f97316;
  color: white;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: bold;
}
</style>
