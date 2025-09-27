<template>
  <div class="crud-card">
    <h2 class="crud-subtitle">Historial de Registros</h2>
    <table class="crud-table">
      <thead>
        <tr>
          <th>Usuario</th>
          <th>Factura</th>
          <th>Paquetería</th>
          <th>Cantidad</th>
          <th>Clave Producto</th>
          <th>Tipo Embalaje</th>
          <th>Fecha Creación</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="caja in historial" :key="caja.id || caja.numero_factura">
        <td>{{ caja.numero_factura }}</td>
        <td>{{ caja.paqueteria }}</td>
        <td>{{ caja.cantidad_piezas }}</td>
        <td>{{ caja.clave_producto }}</td>
        <td>{{ caja.tipo_embalaje }}</td>
        <td>{{ caja.fecha_creacion }}</td>
        <td>{{ caja.usuario_creador }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CompHistorial",
  data() {
    return { historial: [] };
  },
  created() { this.fetchHistorial(); },
  methods: {
    async fetchHistorial() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/historial/historial/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.historial = response.data;
      } catch (err) {
        console.error("Error al cargar historial:", err);
        alert("No se pudo cargar el historial");
      }
    }
  }
};
</script>

<style scoped>
.crud-table { width: 100%; border-collapse: collapse; }
.crud-table th, .crud-table td { border: 1px solid #ccc; padding: 8px; text-align: left; }
.crud-table th { background-color: #f0f4f8; }
</style>
