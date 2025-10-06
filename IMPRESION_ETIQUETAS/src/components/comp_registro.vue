<template>
  <div class="historial-wrapper">
    <h1>Historial de Pedidos</h1>
    <table class="historial-table">
      <thead>
        <tr>
          <th>Usuario</th>
          <th>Factura</th>
          <th>Cantidad</th>
          <th>Tipo Embalaje</th>
          <th>Paquetería</th>
          <th>Clave Producto</th>
          <th>Tipo Pedido</th>
          <th>Fecha Creación</th>
          <th>Peso Volumétrico</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in historial" :key="item.id">
          <td>{{ item.usuario }}</td>
          <td>{{ item.factura }}</td>
          <td>{{ item.cantidad_piezas }}</td>
          <td>{{ item.tipo_embalaje }}</td>
          <td>{{ item.paqueteria }}</td>
          <td>{{ item.clave_producto }}</td>
          <td>{{ item.tipo_pedido }}</td>
          <td>{{ formatFecha(item.fecha_creacion) }}</td>
          <td>{{ item.peso_volumetrico }}</td>
          <td>
            <button @click="editar(item)">Editar</button>
            <button @click="eliminar(item)">Eliminar</button>
          </td>
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
    return {
      historial: []
    };
  },
  mounted() {
    this.fetchHistorial();
  },
  methods: {
    async fetchHistorial() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/historial/registros/");
        this.historial = res.data;
      } catch (error) {
        console.error("Error al cargar historial:", error);
        alert("Error al cargar historial");
      }
    },
    formatFecha(fecha) {
      return new Date(fecha).toLocaleString();
    },
    editar(item) {
      // Aquí podrías redirigir a un formulario de edición
      alert(`Editar ${item.tipo_pedido} ID: ${item.id}`);
    },
    async eliminar(item) {
      try {
        const url = item.tipo_pedido === "Caja"
          ? `http://127.0.0.1:8000/historial/caja/${item.id}`
          : `http://127.0.0.1:8000/historial/tarima/${item.id}`;
        await axios.delete(url);
        alert(`${item.tipo_pedido} eliminada correctamente`);
        this.fetchHistorial(); // refrescar tabla
      } catch (error) {
        console.error("Error al eliminar:", error);
        alert("Error al eliminar registro");
      }
    }
  }
};
</script>

<style scoped>
.historial-wrapper {
  padding: 20px;
  font-family: "Poppins", sans-serif;
}

.historial-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.historial-table th,
.historial-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.historial-table th {
  background-color: #0f1973;
  color: white;
}

.historial-table tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

.historial-table button {
  margin: 2px;
  padding: 5px 10px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.historial-table button:hover {
  opacity: 0.8;
}
</style>
