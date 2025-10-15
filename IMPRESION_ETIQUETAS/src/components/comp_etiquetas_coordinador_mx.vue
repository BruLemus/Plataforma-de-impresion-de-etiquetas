<template>
  <div class="app-container">
    <!-- BARRA SUPERIOR -->
    <header class="header no-print">
      <div class="header-content">
        <h1 class="logo">
          <i class="fas fa-box"></i> Proceso de Embalaje <span class="green-dot">MX</span>
        </h1>
        <h2 class="coordinador-title">
          <i class="fas fa-user-tie"></i> Coordinador 
        </h2>
        <div class="user-info"> 
          <i class="fas fa-clock"></i> Entrada: <strong v-if="horaEntrada">{{ horaEntrada }}</strong> |
          <button class="btn-logout" @click="logout"><i class="fas fa-sign-out-alt"></i> Salir</button>
        </div>
      </div>
    </header>

    <!-- LAYOUT -->
    <div class="layout">
      <!-- SIDEBAR -->
      <aside class="sidebar no-print">
        <nav class="menu">
          <ul>
            <div class="sidebar-user" @click="setView('crear_practicante')" style="cursor:pointer;">
            <i class="fas fa-user-circle"></i>
            <span>{{ username }}</span>
          </div>

            <li :class="{active: currentView === 'caja'}" @click="setView('caja')">
              <i class="fas fa-box-open"></i> Etiquetas por Caja
            </li>
            <li :class="{active: currentView === 'tarima'}" @click="setView('tarima')">
              <i class="fas fa-warehouse"></i> Etiquetas por Tarima
            </li>
            <li :class="{active: currentView === 'otras_etiquetas'}" @click="setView('otras_etiquetas')">
              <i class="fas fa-exclamation-triangle"></i> Otras Etiquetas
            </li>
            <li :class="{active: currentView === 'historial'}" @click="setView('historial')">
              <i class="fas fa-chart-bar"></i> Registros
            </li>
            <li :class="{active: currentView === 'info'}" @click="setView('info')">
              <i class="fas fa-info-circle"></i> Acerca de . . .
            </li>
          </ul>
        </nav>
      </aside>

      <!-- CONTENIDO PRINCIPAL -->
      <main class="content">
        <!-- ETIQUETAS POR CAJA -->
        <section v-if="currentView === 'caja'">
          <div class="crud-card no-print">
            <h2 class="crud-subtitle">Etiquetas por Caja</h2>

            <!-- FORMULARIO -->
            <div class="form-grid">
              <div class="form-field">
                <label class="crud-label">Paquetería</label>
                <select v-model="paqueteriaSeleccionada" class="crud-input">
                  <option disabled value="">-- Selecciona --</option>
                  <option v-for="paq in paqueterias" :key="paq.nombre" :value="paq">{{ paq.nombre }}</option>
                </select>
              </div>

              <div class="form-field">
                <label class="crud-label">Número de Factura</label>
                <input v-model="factura" type="text" class="crud-input" placeholder="Factura" />
              </div>

              <div class="form-field">
                <label class="crud-label">Número de Cajas</label>
                <input v-model.number="numCajas" type="number" min="0" class="crud-input" placeholder="Ej: 3" />
              </div>

              <div class="form-field">
                <label class="crud-label">Tipo de Embalaje</label>
                <select v-model="tipoEmbalaje" class="crud-input">
                  <option disabled value="">-- Selecciona --</option>
                  <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
                </select>
              </div>

              <div class="form-field">
                <label class="crud-label">Clave de Producto</label>
                <input v-model="claveProducto" type="text" class="crud-input" placeholder="Clave del producto" />
              </div>

              <!-- SOLO PARA ESTAFETA Y PAQUETEXPRESS -->
              <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'" class="form-field">
                <label class="crud-label">Ancho de la Caja (cm)</label>
                <input v-model.number="anchoCaja" type="number" min="0" class="crud-input" placeholder="Ej: 40" />
              </div>
              <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'" class="form-field">
                <label class="crud-label">Alto de la Caja (cm)</label>
                <input v-model.number="altoCaja" type="number" min="0" class="crud-input" placeholder="Ej: 60" />
              </div>
              <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'" class="form-field">
                <label class="crud-label">Largo de la Caja (cm)</label>
                <input v-model.number="largoCaja" type="number" min="0" class="crud-input" placeholder="Ej: 50" />
              </div>

              <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'" class="form-field">
                <label class="crud-label">Peso (kg)</label>
                <input v-model.number="peso" type="number" min="0" step="0.01" class="crud-input" placeholder="Ej: 2.5" />
              </div>

              <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'" class="form-field">
                <label class="crud-label">Peso Volumétrico (kg)</label>
                <input :value="pesoVolumetrico.toFixed(2)" type="number" class="crud-input" disabled />
              </div>
            </div>

            <!-- PIEZAS POR CAJA -->
            <div v-if="numCajas > 0" class="mb-4">
              <h3 class="crud-subtitle">Piezas por Caja</h3>
              <div class="pieces-grid">
                <div v-for="n in numCajas" :key="n" class="piece-card">
                  <label class="crud-label-inline">Caja {{ n }}</label>
                  <input v-model.number="piezas[n-1]" type="number" min="0" class="crud-input-small" placeholder="0" />
                </div>
              </div>
            </div>

            <!-- BOTONES CRUD CENTRADOS -->
            <div class="crud-actions centered no-print">
              <button @click="imprimirZebra" class="btn btn-print">
                <i class="fas fa-print"></i> Imprimir en Zebra
              </button>
              
              <button @click="reiniciar" class="btn btn-reset">
                <i class="fas fa-redo-alt"></i> Reiniciar
              </button>
              <button @click="guardarDatos" class="btn btn-save">
                <i class="fas fa-save"></i> Guardar
              </button>
            </div>
          </div>

          <!-- ETIQUETAS PARA IMPRESIÓN -->
          <div class="labels-container print-only" v-if="numCajas > 0">
            <div v-for="n in numCajas" :key="'etiqueta-' + n" class="etiqueta">
              <div class="contenido">
                <div class="logo-wrapper">
                  <img :src="paqueteriaSeleccionada.logo" :alt="paqueteriaSeleccionada.nombre + ' Logo'" class="logo-etiqueta" />
                </div>
                <div class="etiqueta-content">
                  <div class="etiqueta-datos">
                    <div class="dato"><strong>Factura:</strong> {{ factura || '—' }}</div>
                    <div class="dato"><strong>Caja:</strong> {{ n }} de {{ numCajas }}</div>
                    <div class="dato"><strong>Piezas:</strong> {{ piezas[n-1] || 0 }}</div>
                    <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'">
                      <div class="dato"><strong>Ancho:</strong> {{ anchoCaja || 0 }} cm</div>
                      <div class="dato"><strong>Alto:</strong> {{ altoCaja || 0 }} cm</div>
                      <div class="dato"><strong>Largo:</strong> {{ largoCaja || 0 }} cm</div>
                      <div class="dato"><strong>Peso:</strong> {{ peso || 0 }} kg</div>
                      <div class="dato"><strong>Peso Volumétrico:</strong> {{ pesoVolumetrico.toFixed(2) }} kg</div>
                    </div>
                  </div>
                  <div class="etiqueta-qr">
                    <qrcode-vue :value="generateQR(n-1)" :size="qrSize" level="H" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- OTROS COMPONENTES -->
        <section v-if="currentView === 'tarima'"><comp_tarima_mx /></section>
        <section v-if="currentView === 'otras_etiquetas'"><comp_otras_etiquetas /></section>
        <section v-if="currentView === 'historial'"><comp_historial_mx /></section>
        <section v-if="currentView === 'info'"><comp_inf /></section>
        <section v-if="currentView === 'crear_practicante'"><comp_crear_practicante_mx /></section>
      </main>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import QrcodeVue from "qrcode.vue";
import comp_tarima_mx from "@/components/comp_tarima_mx.vue";
import comp_inf from "@/components/comp_inf.vue";
import comp_otras_etiquetas from "./comp_otras_etiquetas.vue";
import comp_historial_mx from "./comp_historial_mx.vue";
import comp_crear_practicante_mx from "./comp_crear_practicante_mx.vue"

export default {
  name: "dashboard_coordinadores_mx",
  components: { QrcodeVue, comp_tarima_mx, comp_inf, comp_otras_etiquetas, comp_historial_mx, comp_crear_practicante_mx},
  data() {
    return {
      username: localStorage.getItem("username") || "",
      horaEntrada: localStorage.getItem("horaEntrada") || "",
      currentView: "caja",
      showEditUserModal: false,
      editUser: { nombre: "", contrasena: "" },
      paqueterias: [
        { nombre: "Paquetexpress", logo: new URL("@/assets/pExp.png", import.meta.url).href },
        { nombre: "FedEx", logo: new URL("@/assets/fedex.png", import.meta.url).href },
        { nombre: "DHL", logo: new URL("@/assets/dhl.png", import.meta.url).href },
        { nombre: "Estafeta", logo: new URL("@/assets/estafeta.png", import.meta.url).href },
        { nombre: "Mercado Libre", logo: new URL("@/assets/mercadolibre.png", import.meta.url).href },
        { nombre: "UPS", logo: new URL("@/assets/ups.png", import.meta.url).href },
      ],
      paqueteriaSeleccionada: { nombre: "", logo: "" },
      factura: "",
      numCajas: 0,
      piezas: [],
      tipoEmbalaje: "",
      claveProducto: "",
      anchoCaja: "",
      altoCaja: "",
      largoCaja: "",
      peso: "",
      qrSize: 130,
      impresoraOnline: false,
      nombrePracticante: localStorage.getItem("username") || "",
      nombreCoordinador: "Coordinador Principal",
    };
  },
  computed: {
    totalPiezas() { return this.piezas.reduce((acc, val) => acc + (Number(val) || 0), 0); },
    pesoVolumetrico() {
      if (this.anchoCaja && this.altoCaja && this.largoCaja) {
        return (this.anchoCaja * this.altoCaja * this.largoCaja) / 5000; //PESO VOLUMETRICO ENTRE 5000 -----------------------------------------------
      }
      return 0;
    },
  },
  created() {
    const hora = new Date().toLocaleString();
    localStorage.setItem("horaEntrada", hora);
    this.horaEntrada = hora;
    this.checkPrinterStatus();
    setInterval(this.checkPrinterStatus, 5000);
  },
  methods: {
    setView(view) { this.currentView = view; },
    openEditUserModal() { this.showEditUserModal = true; },
    closeEditUserModal() { this.showEditUserModal = false; },
    saveUser() { alert("Función de guardar usuario aquí"); },
    logout() { localStorage.clear();this.$router.push("/") },
    goToCrearPracticante() {
      this.$router.push('/crearpracticante_mx');
    },
    checkPrinterStatus() { this.impresoraOnline = true; },
    reiniciar() {
      this.factura = "";
      this.numCajas = 0;
      this.piezas = [];
      this.tipoEmbalaje = "";
      this.claveProducto = "";  
      this.anchoCaja = "";
      this.altoCaja = "";
      this.largoCaja = "";
      this.peso = "";
    },
    imprimirZebra() { alert("Impresión en Zebra"); },
    imprimirRemoto() { alert("Impresión Servidor/ZPL"); },
    generateQR(index) { return `Factura:${this.factura || "—"}|Caja:${index+1}|Practicante:${this.nombrePracticante}`; },

async guardarDatos() {
  // Validar campos obligatorios
  if (!this.paqueteriaSeleccionada.nombre || !this.factura || !this.numCajas || !this.tipoEmbalaje || !this.claveProducto) {
    alert("Completa los campos obligatorios.");
    return;
  }

  // Total de piezas
  const totalPiezas = this.piezas.reduce((acc, val) => acc + (Number(val) || 0), 0);

  // IDs desde localStorage
  const practicante_id = Number(localStorage.getItem("practicante_id")) || 0;
  const coordinador_id = Number(localStorage.getItem("coordinador_id")) || 5; // por ejemplo

  // Nombres desde localStorage
  const nombrePracticante = localStorage.getItem("nombre_practicante") || this.nombrePracticante || "string";
  const nombreCoordinador = localStorage.getItem("nombre_coordinador") || this.nombreCoordinador || "String";

  // Token JWT
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Inicia sesión nuevamente.");
    return;
  }

  // Estructura del payload
  const payload = {
    nombre_user_practicante: nombrePracticante,
    nombre_user_coordinador: nombreCoordinador,
    n_facturas: String(this.factura),
    n_cajas: Number(this.numCajas),
    paqueteria: this.paqueteriaSeleccionada.nombre,
    t_embalaje: Number(this.tipoEmbalaje),
    clave_producto: String(this.claveProducto),
    cantidad_piezas: totalPiezas,
    ancho: Number(this.anchoCaja) || 0,
    largo: Number(this.largoCaja) || 0,
    alto: Number(this.altoCaja) || 0,
    peso: Number(this.peso) || 0,
    peso_volumetrico: Number(this.pesoVolumetrico.toFixed(2)) || 0,
    practicante_id,
    coordinador_id
  };

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/cajas_mx/?sede=mexico&role=coordinador",
      payload,
      {
        headers: {
          "accept": "application/json",
          "Content-Type": "application/json",
          "token": token
        }
      }
    );

    console.log("✅ Respuesta API:", response.data);
    alert("✅ Datos guardados correctamente");
    this.reiniciar();

  } catch (error) {
    console.error("❌ Error en API:", error.response || error);
    const msg = error.response?.data?.detail || "Error al guardar. Revisa los datos.";
    alert(msg);
  }
}





  },
};
</script>





<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');


.green-dot {
  color: #22c55e;
  font-weight: bold;
 
}

/* ==== VARIABLES ==== */
:root {
  --bg: #f9fafb;
  --card: #ffffff;
  --muted: #6b7280;
  --primary-dark: #131a2e;
  --primary: #4274c4;
  --secondary: #f97316; /* Naranja Coordinador */
  --accent: #facc15;
  --text: #111827;
  --field-bg: #f9fafb;
  --shadow: 0 6px 18px rgba(0,0,0,0.08);
}

/* ==== LAYOUT GENERAL ==== */
.app-container {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  flex-direction: column;
  font-family: 'Poppins', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color: var(--text);
}
.layout {
  display: flex;
  flex: 1;
  margin-top: 60px;
}

/* ==== BARRA SUPERIOR ==== */
.header {
  background: linear-gradient(to right, #031021, #0b22a1); /* De rojo oscuro a rojo vivo */
  color: #c4cdd9;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
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
.logo {
  font-size: 1.4rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
}
.coordinador-title {

  font-size: 1.5rem;
  font-weight: 700;
  color: #ef4444;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
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
  color: #060b14;
  border: none;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}
.btn-logout:hover {
  background: #b0adad;
}

/* ==== SIDEBAR ==== */
.sidebar {
  width: 220px;
  background: #1e293b;
  color: white;
  padding-top: 20px;
  min-height: calc(100vh - 60px);
}
.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
  padding-top: 20px;
}
.menu li {
  padding: 12px 20px;
  cursor: pointer;
  font-weight: 500;
  border-left: 4px solid transparent;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.menu li:hover { background: #334155; }
.menu li.active { background: #3567b6; border-left: 4px solid var(--accent); }

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  margin-bottom: 20px;
  cursor: pointer;
  font-weight: 600;
}

/* ==== CONTENIDO ==== */
.content { flex: 1; padding: 20px; background: var(--bg); }

/* ==== FORMULARIO ==== */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}
.form-field {
  background: var(--field-bg);
  border-radius: 12px;
  padding: 14px 18px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.2s;
}
.form-field:hover { box-shadow: 0 6px 18px rgba(0,0,0,0.12); }
.crud-label {
  font-weight: 600;
  margin-bottom: 8px;
  display: block;
  color: #1e3a8a;
}
.crud-input {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  width: 100%;
  padding: 10px;
  font-size: 0.95rem;
  transition: all 0.2s;
}
.crud-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 5px rgba(37, 99, 235, 0.3);
}

/* ==== PIEZAS POR CAJA ==== */
.pieces-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}
.piece-card {
  background: #feebe0;
  border-radius: 10px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 90px;
  transition: all 0.2s;
}
.piece-card:hover { background: #bae6fd; }
.crud-label-inline {
  font-weight: 600;
  margin-bottom: 6px;
  text-align: center;
}
.crud-input-small {
  border: 1px solid #9ca3af;
  border-radius: 6px;
  width: 60px;
  padding: 6px;
  font-size: 0.9rem;
  text-align: center;
}

/* ==== CRUD GENERAL ==== */
.crud-card {
  background: var(--card);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  transition: all 0.3s;
}
.crud-card:hover {
  box-shadow: 0 10px 28px rgba(0,0,0,0.16);
}
 .crud-subtitle { font-size: 28px; font-weight: 700; color: #1f618d; margin-bottom: 20px; border-left: 6px solid #2980b9; padding-left: 12px; }

/* ==== BOTONES ==== */
.crud-actions.centered {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
}
.btn {
  padding: 10px 18px;
  font-weight: 600;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
.btn:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.12); }
.btn-print { background: #126330; color: white; }
.btn-print:hover { background: #0f4f27; }
.btn-reset { background: #cd981c; color: white; }
.btn-reset:hover { background: #b47f16; }
.btn-save { background: #2559ac; color: white; }
.btn-save:hover { background: #1e418c; }

/* ==== ETIQUETAS ==== */
.labels-container {
  display: flex;
  flex-wrap: wrap;

  gap: 16px;
  margin-top: 20px;
  width: 100%;
}
.etiqueta {
  background: var(--card);
  border-radius: 10px;
  padding: 14px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  page-break-inside: avoid;
  width: 100%;
}
.etiqueta-content {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 50px;
}
.logo-etiqueta { width: 120px; margin-bottom: 8px; }
.etiqueta-datos { font-size: 1rem; }
.etiqueta-datos .dato { margin-bottom: 12px; }
.etiqueta-qr { margin-left: 0px; }

/* ==== ESTADO IMPRESORA ==== */
.printer-status {
  background: #f3f4f6;
  color: #111827;
  font-weight: bold;
  text-align: center;
  padding: 8px;
  border-bottom: 2px solid #e5e7eb;
}
.online { color: #22c55e; font-weight: bold; }
.offline { color: #ef4444; font-weight: bold; }

/* ==== MODAL ==== */
.modal-overlay {
  position: fixed;
  top:0; left:0; right:0; bottom:0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
}
.modal-card {
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}
.modal-card h3 { margin-bottom: 16px; color: #1e40af; }
.modal-card .form-field { margin-bottom: 12px; }
.modal-card .form-field label { font-weight: 600; margin-bottom: 4px; display: block; }
.modal-card .form-field input { width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #d1d5db; }

/* ==== IMPRESIÓN ==== */
@media print {
  @page { size: auto; margin: 0; }
  body { background: none !important; }
  body * { visibility: hidden; background: none !important; box-shadow: none !important; }
  .labels-container, .labels-container * { visibility: visible; background: none !important; box-shadow: none !important; color: black !important; }
  .labels-container { position: absolute; top: 0; left: 0; width: 100%; }
  .etiqueta { display: block; margin: 0; width: 100%; background: none !important; box-shadow: none !important; }  
  .no-print { display: none !important; }
}

</style>
