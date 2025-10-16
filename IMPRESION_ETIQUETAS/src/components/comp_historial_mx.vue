<template>
  <div class="crud-card">
    <h2 class="crud-subtitle">📦 Historial de Registros MX</h2>

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

    <!-- Tabla de historial -->
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
          <td>{{ registro.factura || registro.numero_factura || registro.n_facturas }}</td>
          <td>{{ registro.cantidad || registro.cantidad_piezas }}</td>
          <td>{{ registro.tipo_embalaje }}</td>
          <td>{{ registro.paqueteria }}</td>
          <td>{{ registro.clave_producto }}</td>
          <td>{{ registro.largo }}</td>
          <td>{{ registro.ancho }}</td>
          <td>{{ registro.alto }}</td>
          <td>{{ registro.peso }}</td>
          <td>{{ registro.peso_volumetrico?.toFixed(2) }}</td>
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

    <!-- Modal de edición -->
    <div v-if="mostrarModal" class="modal-overlay">
      <div class="modal-content">
        <h3>{{ tituloModal }}</h3>

        <div class="modal-body">
          <!-- Número de factura -->
          

          <!-- Paquetería -->
          <label>Paquetería:</label>
          <select v-model="registroEditando.paqueteria">
            <option v-for="op in opcionesPaqueteria" :key="op" :value="op">{{ op }}</option>
          </select>

          <!-- Tipo de embalaje -->
          <label>Tipo Embalaje:</label>
          <select v-model.number="registroEditando.tipo_embalaje">
            <option v-for="op in opcionesTipoEmbalaje" :key="op" :value="Number(op)">{{ op }}</option>
          </select>

          <!-- Número de tarimas (solo si es Tarima) -->
          <label v-if="registroEditando.tipo_pedido === 'Tarima'">Número de tarimas:</label>
          <input
            v-if="registroEditando.tipo_pedido === 'Tarima'"
            v-model.number="registroEditando.numero_tarimas"
            type="number"
            min="1"
          />

          <!-- Clave de producto -->
          <label>Clave de producto:</label>
          <input v-model="registroEditando.clave_producto" type="text" />

          <!-- Cantidad de piezas -->
          <label>Cantidad de piezas:</label>
          <input
            v-model.number="registroEditando.cantidad_piezas"
            type="number"
            min="1"
          />

          <!-- Dimensiones -->
          <label>Largo (cm):</label>
          <input
            v-model.number="registroEditando.largo"
            type="number"
            min="0"
            step="0.1"
            @input="actualizarPesoVolumetrico"
          />

          <label>Ancho (cm):</label>
          <input
            v-model.number="registroEditando.ancho"
            type="number"
            min="0"
            step="0.1"
            @input="actualizarPesoVolumetrico"
          />

          <label>Alto (cm):</label>
          <input
            v-model.number="registroEditando.alto"
            type="number"
            min="0"
            step="0.1"
            @input="actualizarPesoVolumetrico"
          />

          <!-- Peso -->
          <label>Peso (kg):</label>
          <input v-model.number="registroEditando.peso" type="number" min="0" step="0.01" />

          <!-- Peso volumétrico -->
          <label>Peso Volumétrico (kg):</label>
          <input :value="registroEditando.peso_volumetrico?.toFixed(2)" type="number" disabled />
        </div>

        <div class="modal-footer">
          <button @click="guardarEdicion" class="btn btn-edit">Guardar</button>
          <button @click="cerrarModal" class="btn btn-delete">Cancelar</button>
        </div>
      </div>
    </div>

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
      opcionesPaqueteria: ["Paquetexpress", "Estafeta", "DHL", "FedEx", "UPS", "MercadoLibre"],
      opcionesTipoEmbalaje: ["1", "2", "3", "4", "5"],
      mostrarModal: false,
      registroEditando: null,
    };
  },
  computed: {
    facturaEditable: {
      get() {
        if (!this.registroEditando) return '';
        return this.registroEditando.tipo_pedido === 'Caja'
          ? this.registroEditando.n_facturas
          : this.registroEditando.numero_facturas;
      },
      set(value) {
        if (!this.registroEditando) return;
        if (this.registroEditando.tipo_pedido === 'Caja') {
          this.registroEditando.n_facturas = value;
        } else {
          this.registroEditando.numero_facturas = value;
        }
      },
    },
    historialFiltrado() {
      return this.historial.filter((r) => {
        const texto = this.busqueda.toLowerCase();
        const coincideBusqueda =
          r.nombre_usuario?.toLowerCase().includes(texto) ||
          (r.factura && r.factura.toLowerCase().includes(texto)) ||
          (r.numero_factura && r.numero_factura.toLowerCase().includes(texto)) ||
          (r.n_facturas && r.n_facturas.toLowerCase().includes(texto)) ||
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
    tituloModal() {
      if (!this.registroEditando) return "";
      return this.registroEditando.tipo_pedido === "Caja" ? "Editar Caja" : "Editar Tarima";
    },
  },
  created() {
    this.fetchHistorial();
    this.generarSemanas();
    this.semanaSeleccionada = this.getWeekNumber(new Date()).week;
  },
  methods: {
    getWeekNumber(date) {
      const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
      const dayNum = d.getUTCDay() || 7;
      d.setUTCDate(d.getUTCDate() + 4 - dayNum);
      const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
      const weekNo = Math.ceil(((d - yearStart) / 86400000 + 1) / 7);
      return { year: d.getUTCFullYear(), week: weekNo };
    },
    generarSemanas() {
      this.semanasDisponibles = Array.from({ length: 52 }, (_, i) => i + 1);
    },
    async fetchHistorial() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/registros_mx/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.historial = response.data;
      } catch (err) {
        console.error("Error al cargar historial:", err);
        alert("No se pudo cargar el historial");
      }
    },
    editarRegistro(registro) {
      this.registroEditando = { ...registro };
      this.actualizarPesoVolumetrico();
      this.mostrarModal = true;
    },
    cerrarModal() {
      this.mostrarModal = false;
      this.registroEditando = null;
    },
    actualizarPesoVolumetrico() {
      if (!this.registroEditando) return;
      const { largo, ancho, alto } = this.registroEditando;
      if (largo && ancho && alto) {
        this.registroEditando.peso_volumetrico = (largo * ancho * alto) / 5000;
      } else {
        this.registroEditando.peso_volumetrico = 0;
      }
    },
    async guardarEdicion() {
      if (!this.registroEditando) return;
      const tipo = this.registroEditando.tipo_pedido;
      const url =
        tipo === "Caja"
          ? `http://127.0.0.1:8000/registros_mx/caja/${this.registroEditando.id}`
          : `http://127.0.0.1:8000/registros_mx/tarima/${this.registroEditando.id}`;
      try {
        const token = localStorage.getItem("token");
        await axios.put(url, this.registroEditando, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.fetchHistorial();
        this.cerrarModal();
        alert(`✅${tipo} actualizada correctamente`);
      } catch (err) {
        console.error(`Error al editar ${tipo}:`, err);
        alert(`No se pudo editar la ${tipo.toLowerCase()}`);
      }
    },
    async eliminarRegistro(registro) {
      if (!confirm(`¿Eliminar ${registro.tipo_pedido} ${registro.factura || registro.numero_factura || registro.n_facturas}?`)) return;
      try {
        const token = localStorage.getItem("token");
        const url =
          registro.tipo_pedido === "Caja"
            ? `http://127.0.0.1:8000/registros_mx/caja/${registro.id}`
            : `http://127.0.0.1:8000/registros_mx/tarima/${registro.id}`;
        await axios.delete(url, { headers: { Authorization: `Bearer ${token}` } });
        this.fetchHistorial();
      } catch (err) {
        console.error("Error al eliminar:", err);
        alert("No se pudo eliminar el registro");
      }
    },
    exportarExcel() {
      const ws = XLSX.utils.json_to_sheet(
        this.historialFiltrado.map((r) => ({
          Usuario: r.nombre_usuario,
          Factura: r.factura || r.numero_factura || r.n_facturas,
          Cantidad: r.cantidad || r.cantidad_piezas,
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
  const doc = new jsPDF({
    orientation: 'landscape', 
    unit: 'mm',
    format: 'a4'
  });

  doc.text("Historial de Registros", 14, 10);

  autoTable(doc, {
    head: [
      [
        "Usuario",
        "Factura",
        "Cantidad",
        "Tipo Embalaje",
        "Paquetería",
        "Clave Producto",
        "Largo",
        "Ancho",
        "Alto",
        "Peso",
        "Peso Volumétrico",
        "Tipo Pedido",
        "Fecha Creación",
      ],
    ],
    body: this.historialFiltrado.map((r) => [
      r.nombre_usuario,
      r.factura || r.numero_factura || r.n_facturas,
      r.cantidad || r.cantidad_piezas,
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
    styles: {
      fontSize: 8,          
      cellWidth: 'wrap',    
      overflow: 'linebreak',
    },
    headStyles: {
      fillColor: [41, 128, 185], 
      textColor: 255,
      halign: 'center',
    },
    bodyStyles: {
      halign: 'center',
      valign: 'middle',
    },
    tableWidth: 'auto', 
    margin: { top: 20, left: 10, right: 10 },
  });

  doc.save("Registros.pdf");
}

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
.btn { cursor: pointer; padding: 6px 12px; border-radius: 8px; border: none; color: white; font-weight: bold; margin-right: 6px; }
.btn-edit { background: #3498db; }
.btn-delete { background: #e74c3c; }
.btn-excel { background: #27ae60; }
.btn-pdf { background: #c0392b; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 999; }
.modal-content { background: white; padding: 20px; border-radius: 12px; width: 500px; max-height: 90%; overflow-y: auto; }
.modal-body { display: flex; flex-direction: column; gap: 10px; margin-top: 12px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px; }
.modal-body label { font-weight: 600; }
.modal-body input, .modal-body select { padding: 6px 10px; border-radius: 8px; border: 1px solid #ccc; width: 100%; }
</style>
