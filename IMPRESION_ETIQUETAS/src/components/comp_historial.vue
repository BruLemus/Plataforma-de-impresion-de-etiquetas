<template>
  <div class="crud-card">
    <h2 class="crud-subtitle">📦 Historial de Registros</h2>

    <!-- Controles de búsqueda y filtros -->
    <div class="controls">
      <input 
        type="text" 
        v-model="busqueda" 
        placeholder="🔍 Buscar por usuario, factura, clave o fecha..." 
        class="search-input"
      />

      <select v-model="filtroTipo" class="filter-select">
        <option value="Todos">Todos</option>
        <option value="Caja">Cajas</option>
        <option value="Tarima">Tarimas</option>
      </select>

      <!-- Filtro solo por semana -->
      <div class="date-range">
        <label>Semana:</label>
        <select v-model="semanaSeleccionada" class="filter-select">
          <option v-for="w in semanasDisponibles" :key="w" :value="w">
            Semana {{ w }}
          </option>
        </select>
      </div>

      <button @click="exportarExcel" class="btn btn-excel">⬇️ Excel</button>
      <button @click="exportarPDF" class="btn btn-pdf">⬇️ PDF</button>
    </div>

    <table class="crud-table">
      <thead>
        <tr>
          <th>Usuario</th>
          <th>Factura</th>
          <th>Cantidad</th>
          <th>Tipo Embalaje</th>
          <th>Paquetería</th>
          <th>Clave Producto</th>
          <th>Largo</th>
          <th>Ancho</th>
          <th>Alto</th>
          <th>Peso</th>
          <th>Peso Volumétrico</th>
          <th>Tipo Pedido</th>
          <th>Fecha Creación</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="registro in historialFiltrado" :key="registro.tipo_pedido + registro.id">
          <td>{{ registro.nombre_usuario }}</td>
          <td>{{ registro.factura }}</td>
          <td>{{ registro.cantidad }}</td>
          <td>{{ registro.tipo_embalaje }}</td>
          <td>{{ registro.paqueteria }}</td>
          <td>{{ registro.clave_producto }}</td>
          <td>{{ registro.largo }}</td>
          <td>{{ registro.ancho }}</td>
          <td>{{ registro.alto }}</td>
          <td>{{ registro.peso }}</td>
          <td>{{ registro.peso_volumetrico }}</td>
          <td>
            <span :class="registro.tipo_pedido === 'Caja' ? 'badge-caja' : 'badge-tarima'">
              {{ registro.tipo_pedido }}
            </span>
          </td>
          <td>{{ new Date(registro.fecha_creacion).toLocaleString() }}</td>
          <td>
            <button @click="editarRegistro(registro)" class="btn btn-edit">✏️</button>
            <button @click="eliminarRegistro(registro)" class="btn btn-delete">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import * as XLSX from "xlsx";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export default {
  name: "CompHistorial",
  data() {
    return {
      historial: [],
      busqueda: "",
      filtroTipo: "Todos",
      semanaSeleccionada: null,
      semanasDisponibles: [],
      opcionesPaqueteria: ["Paquetexpress","Estafeta","DHL","FedEx","UPS","MercadoLibre"], 
      opcionesTipoEmbalaje: ["1","2","3","4","5"], 
    };
  },
  created() {
    this.fetchHistorial();
    this.generarSemanas();
    this.semanaSeleccionada = this.getWeekNumber(new Date()).week; // selecciona semana actual
  },
  computed: {
    historialFiltrado() {
      return this.historial.filter(r => {
        const texto = this.busqueda.toLowerCase();
        const coincideBusqueda =
          r.nombre_usuario?.toLowerCase().includes(texto) ||
          r.factura?.toLowerCase().includes(texto) ||
          r.clave_producto?.toLowerCase().includes(texto);

        const coincideTipo = this.filtroTipo === "Todos" || r.tipo_pedido === this.filtroTipo;

        let coincideSemana = true;
        if (this.semanaSeleccionada) {
          const { week } = this.getWeekNumber(new Date(r.fecha_creacion));
          coincideSemana = week === this.semanaSeleccionada;
        }

        return coincideBusqueda && coincideTipo && coincideSemana;
      });
    },
  },
  methods: {
    getWeekNumber(date) {
      const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
      const dayNum = d.getUTCDay() || 7;
      d.setUTCDate(d.getUTCDate() + 4 - dayNum);
      const yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
      const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1)/7);
      return { year: d.getUTCFullYear(), week: weekNo };
    },

    generarSemanas() {
      this.semanasDisponibles = Array.from({length: 52}, (_, i) => i + 1);
    },

    async fetchHistorial() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/historial/registros/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.historial = response.data;
      } catch (err) {
        console.error("Error al cargar historial:", err);
        alert("No se pudo cargar el historial");
      }
    },

    exportarExcel() {
      const ws = XLSX.utils.json_to_sheet(
        this.historialFiltrado.map(r => ({
          Usuario: r.nombre_usuario,
          Factura: r.factura,
          Cantidad: r.cantidad,
          "Tipo Embalaje": r.tipo_embalaje,
          Paquetería: r.paqueteria,
          "Clave Producto": r.clave_producto,
          Largo: r.largo,
          Ancho: r.ancho,
          Alto: r.alto,
          Peso: r.peso,
          "Peso Volumétrico": r.peso_volumetrico,
          "Tipo Pedido": r.tipo_pedido,
          "Fecha Creación": new Date(r.fecha_creacion).toLocaleString(),
        }))
      );
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Historial");
      XLSX.writeFile(wb, "Registros.xlsx");
    },

    exportarPDF() {
      const doc = new jsPDF();
      doc.text("Historial de Registros", 14, 10);
      autoTable(doc, {
        head: [[
          "Usuario","Factura","Cantidad","Tipo Embalaje","Paquetería","Clave Producto",
          "Largo","Ancho","Alto","Peso","Peso Volumétrico","Tipo Pedido","Fecha Creación"
        ]],
        body: this.historialFiltrado.map(r => [
          r.nombre_usuario,
          r.factura,
          r.cantidad,
          r.tipo_embalaje,
          r.paqueteria,
          r.clave_producto,
          r.largo,
          r.ancho,
          r.alto,
          r.peso,
          r.peso_volumetrico,
          r.tipo_pedido,
          new Date(r.fecha_creacion).toLocaleString(),
        ]),
      });
      doc.save("Registros.pdf");
    },

    async eliminarRegistro(registro) {
      if (!confirm(`¿Eliminar ${registro.tipo_pedido} ${registro.factura}?`)) return;
      try {
        const token = localStorage.getItem("token");
        const url =
          registro.tipo_pedido === "Caja"
            ? `http://127.0.0.1:8000/historial/registros/caja/${registro.id}`
            : `http://127.0.0.1:8000/historial/registros/tarima/${registro.id}`;
        await axios.delete(url, { headers: { Authorization: `Bearer ${token}` } });
        this.fetchHistorial();
      } catch (err) {
        console.error("Error al eliminar:", err);
        alert("No se pudo eliminar el registro");
      }
    },

    async editarRegistro(registro) {
      const body = {};

      let nuevoPaquete = prompt(
        `Seleccione Paquetería: ${this.opcionesPaqueteria.join(", ")}`,
        registro.paqueteria || ""
      );
      if (nuevoPaquete && this.opcionesPaqueteria.includes(nuevoPaquete)) body.paqueteria = nuevoPaquete;

      let nuevoEmbalaje = prompt(
        `Seleccione Tipo de Embalaje: ${this.opcionesTipoEmbalaje.join(", ")}`,
        registro.tipo_embalaje || ""
      );
      const numEmbalaje = Number(nuevoEmbalaje);
      if (!isNaN(numEmbalaje) && this.opcionesTipoEmbalaje.includes(nuevoEmbalaje)) body.tipo_embalaje = nuevoEmbalaje;

      const campos = [
        { key: "factura", label: "Número de factura" },
        { key: "cantidad", label: "Cantidad de piezas" },
        { key: "clave_producto", label: "Clave de producto" },
        { key: "largo", label: "Largo" },
        { key: "ancho", label: "Ancho" },
        { key: "alto", label: "Alto" },
        { key: "peso", label: "Peso" },
        { key: "peso_volumetrico", label: "Peso Volumétrico" }
      ];

      for (const campo of campos) {
        const valorActual = registro[campo.key] ?? "";
        let nuevoValor = prompt(`Ingrese nuevo valor para ${campo.label}:`, valorActual);
        if (nuevoValor !== null && nuevoValor !== valorActual) {
          if (["cantidad","largo","ancho","alto","peso","peso_volumetrico"].includes(campo.key)) {
            const num = Number(nuevoValor);
            if (!isNaN(num)) body[campo.key] = num;
            else { alert(`${campo.label} debe ser un número válido`); return; }
          } else if (nuevoValor.trim() !== "") {
            body[campo.key] = nuevoValor;
          }
        }
      }

      if (Object.keys(body).length === 0) return;

      try {
        const token = localStorage.getItem("token");
        const url =
          registro.tipo_pedido === "Caja"
            ? `http://127.0.0.1:8000/historial/registros/caja/${registro.id}`
            : `http://127.0.0.1:8000/historial/registros/tarima/${registro.id}`;
        await axios.put(url, body, { headers: { Authorization: `Bearer ${token}` } });
        this.fetchHistorial();
      } catch (err) {
        console.error("Error al editar:", err);
        alert("No se pudo editar el registro");
      }
    },
  },
};
</script>

<style scoped>
.crud-card { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
.crud-subtitle { font-size: 28px; font-weight: 700; color: #1f618d; margin-bottom: 20px; border-left: 6px solid #2980b9; padding-left: 12px; }
.controls { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin-bottom: 16px; }
.search-input, .filter-select, .date-input { padding: 8px 12px; border: 1px solid #ccc; border-radius: 8px; flex-grow: 1; min-width: 250px; }
.crud-table { width: 100%; border-collapse: collapse; margin-top: 12px; }
.crud-table th, .crud-table td { border: 1px solid #ddd; padding: 12px 10px; text-align: left; }
.crud-table th { background: #2980b9; color: white; }
.crud-table tr:nth-child(even) { background-color: #f4f6f8; }
.crud-table tr:hover { background-color: #d6eaf8; }
.badge-caja { background: #3498db; color: white; padding: 4px 10px; border-radius: 14px; }
.badge-tarima { background: #e67e22; color: white; padding: 4px 10px; border-radius: 14px; }
.btn { padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600; border: none; }
.btn-excel { background: #27ae60; color: white; }
.btn-pdf { background: #c0392b; color: white; }
.btn-edit { background: #2980b9; color: white; margin-right: 4px; }
.btn-delete { background: #c0392b; color: white; }
</style>
