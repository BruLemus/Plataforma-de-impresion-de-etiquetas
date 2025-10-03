<!-- src/components/CompEtiquetasPracticantes.vue -->
<template>
  <div class="app-container">
    <!-- BARRA SUPERIOR -->
    <header class="header no-print">
      <div class="header-content">
        <h1 class="logo">
          <i class="fas fa-box"></i> Proceso de Embalaje
        </h1>
        <h2 class="coordinador-title">
          <i class="fas fa-user-graduate"></i> Practicante
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
            <div class="sidebar-user" @click="openEditUserModal">
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
            
            <li :class="{active: currentView === 'info'}" @click="setView('info')">
              <i class="fas fa-info-circle"></i> Acerca de . . .
            </li>
          </ul>
        </nav>
      </aside>

      <!-- MODAL EDITAR PERFIL -->
      <div v-if="showEditUserModal" class="modal-overlay" @click.self="closeEditUserModal">
        <div class="modal-card">
          <h3>Editar Perfil</h3>

          <div class="form-field">
            <label>Nombre</label>
            <input v-model="editUser.nombre" placeholder="Nombre completo" />
          </div>
          <div class="form-field">
            <label>Contraseña</label>
            <input v-model="editUser.contrasena" type="password" placeholder="Nueva contraseña" />
          </div>

          <div class="crud-actions">
            <button @click="saveUser" class="btn btn-save">
              <i class="fas fa-save"></i> Guardar
            </button>
            <button @click="closeEditUserModal" class="btn btn-reset">
              Cancelar
            </button>
          </div>
        </div>
      </div>

      <!-- CONTENIDO PRINCIPAL -->
      <main class="content">
        <!-- ETIQUETAS POR CAJA -->
        <section v-if="currentView === 'caja'">
          <div class="crud-card no-print">
            <h2 class="crud-subtitle">Etiquetas por Caja</h2>

            <!-- FORMULARIO -->
            <div class="form-grid">
              <!-- Paquetería -->
              <div class="form-field">
                <label class="crud-label">Paquetería</label>
                <select v-model="paqueteriaSeleccionada" class="crud-input">
                  <option disabled value="">-- Selecciona --</option>
                  <option v-for="paq in paqueterias" :key="paq.nombre" :value="paq">{{ paq.nombre }}</option>
                </select>
              </div>

              <!-- Factura -->
              <div class="form-field">
                <label class="crud-label">Número de Factura</label>
                <input v-model="factura" type="text" class="crud-input" placeholder="Factura" />
              </div>

              <!-- Número de cajas -->
              <div class="form-field">
                <label class="crud-label">Número de Cajas</label>
                <input v-model.number="numCajas" type="number" min="0" class="crud-input" placeholder="Ej: 3" />
              </div>

              <!-- Tipo de Embalaje -->
              <div class="form-field">
                <label class="crud-label">Tipo de Embalaje</label>
                <select v-model="tipoEmbalaje" class="crud-input">
                  <option disabled value="">-- Selecciona --</option>
                  <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
                </select>
              </div>

              <!-- Clave de Producto -->
              <div class="form-field">
                <label class="crud-label">Clave de Producto</label>
                <input v-model="claveProducto" type="text" class="crud-input" placeholder="Clave del producto" />
              </div>

              <!-- Peso -->
              <div class="form-field">
                <label class="crud-label">Peso de la Caja (kg)</label>
                <input v-model.number="peso" type="number" min="0" class="crud-input" placeholder="Ej: 15" />
              </div>

              <!-- SOLO SI ES ESTAFETA -->
              <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta'" class="form-field">
                <label class="crud-label">Ancho de la Caja (cm)</label>
                <input v-model.number="anchoCaja" type="number" min="0" class="crud-input" placeholder="Ej: 40" />
              </div>
              <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta'" class="form-field">
                <label class="crud-label">Alto de la Caja (cm)</label>
                <input v-model.number="altoCaja" type="number" min="0" class="crud-input" placeholder="Ej: 60" />
              </div>
              <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta'" class="form-field">
                <label class="crud-label">Largo de la Caja (cm)</label>
                <input v-model.number="largoCaja" type="number" min="0" class="crud-input" placeholder="Ej: 50" />
              </div>
            </div>

            <!-- Piezas -->
            <div v-if="numCajas > 0" class="mb-4">
              <h3 class="crud-subtitle">Piezas por Caja</h3>
              <div class="pieces-grid">
                <div v-for="n in numCajas" :key="n" class="piece-card">
                  <label class="crud-label-inline">Caja {{ n }}</label>
                  <input v-model.number="piezas[n-1]" type="number" min="0" class="crud-input-small" placeholder="0" />
                </div>
              </div>
            </div>

            <!-- ESTATUS DE IMPRESORA -->
            <div class="printer-status no-print">
              <i class="fas fa-print"></i> Estado de Impresora:
              <span :class="{ online: impresoraOnline, offline: !impresoraOnline }">
                {{ impresoraOnline ? "En línea ✅" : "Desconectada ❌" }}
              </span>
            </div>

            <!-- BOTONES -->
            <div class="crud-actions centered no-print">
              <button @click="imprimirZebra" class="btn btn-print">
                <i class="fas fa-print"></i> Imprimir en Zebra
              </button>
              <button @click="imprimirRemoto" class="btn btn-print">
                <i class="fas fa-server"></i> Imprimir en Servidor (ZPL)
              </button>
              <button @click="reiniciar" class="btn btn-reset">
                <i class="fas fa-redo-alt"></i> Reiniciar
              </button>
              <button @click="guardarDatosPracticante" class="btn btn-save">
                <i class="fas fa-save"></i> Guardar
              </button>
            </div>
          </div>

          <!-- ETIQUETAS DE CAJA -->
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
                    <div class="dato"><strong>Peso:</strong> {{ peso || 0 }} kg</div>
                    <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta'">
                      <div class="dato"><strong>Ancho:</strong> {{ anchoCaja || 0 }} cm</div>
                      <div class="dato"><strong>Alto:</strong> {{ altoCaja || 0 }} cm</div>
                      <div class="dato"><strong>Largo:</strong> {{ largoCaja || 0 }} cm</div>
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

        <!-- TARIMA -->
        <section v-if="currentView === 'tarima'"><comp_tarima /></section>

        <!-- OTRAS ETIQUETAS -->
        <section v-if="currentView === 'otras_etiquetas'"><comp_otras_etiquetas /></section>

        <!-- INFO -->
        <section v-if="currentView === 'info'"><comp_inf /></section>
      </main>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import QrcodeVue from "qrcode.vue";
import comp_tarima from "@/components/comp_tarima.vue";
import comp_inf from "@/components/comp_inf.vue";
import comp_otras_etiquetas from "./comp_otras_etiquetas.vue";

export default {
  name: "CompEtiquetasPracticantes",
  components: { QrcodeVue, comp_tarima, comp_inf, comp_otras_etiquetas,  },
  data() {
    return {
      username: localStorage.getItem("username") || "",
      mesaSeleccionada: localStorage.getItem("mesaSeleccionada") || "",
      horaEntrada: "",
      currentView: "caja",
      showEditUserModal: false,
      editUser: { nombre: "", contrasena: "" },
      paqueterias: [
        { nombre: "Paquetexpress", logo: new URL("@/assets/pExp.png", import.meta.url).href },
        { nombre: "FedEx", logo: new URL("@/assets/fedex.png", import.meta.url).href },
        { nombre: "DHL", logo: new URL("@/assets/dhl.png", import.meta.url).href },
        { nombre: "Estafeta", logo: new URL("@/assets/estafeta.png", import.meta.url).href },
        { nombre: "Mercado Libre", logo: new URL("@/assets/mercadolibre.png", import.meta.url).href },
        { nombre: "UPS", logo: new URL("@/assets/ups.png", import.meta.url).href }
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
      impresoraOnline: false
    };
  },
  created() {
    const hora = new Date().toLocaleString();
    localStorage.setItem("horaEntrada", hora);
    this.horaEntrada = hora;
    this.checkPrinterStatus();
    setInterval(this.checkPrinterStatus, 5000);
  },
  computed: {
    totalPiezas() {
      return this.piezas.reduce((acc, val) => acc + (Number(val) || 0), 0);
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/");
    },
    setView(view) {
      this.currentView = view;
    },
    openEditUserModal() {
      this.showEditUserModal = true;
      this.editUser.nombre = this.username;
    },
    closeEditUserModal() {
      this.showEditUserModal = false;
    },
    async saveUser() {
      try {
        const payload = { nombre: this.editUser.nombre, contrasena: this.editUser.contrasena };
        const token = localStorage.getItem("token");
        await axios.put("http://127.0.0.1:8000/user_practicantes/perfil", payload, {
          headers: { Authorization: token ? `Bearer ${token}` : "" }
        });
        this.username = this.editUser.nombre;
        localStorage.setItem("username", this.username);
        alert("Perfil actualizado correctamente");
        this.closeEditUserModal();
      } catch (err) {
        console.error(err);
        if (err.response && err.response.status === 401) alert("Token inválido o expirado. Por favor, inicia sesión de nuevo.");
        else alert("Error al actualizar el perfil");
      }
    },
    generateQR(index) {
      let data = [
        `Factura: ${this.factura || '-'}`,
        `Caja: ${index + 1} de ${this.numCajas || 0}`,
        `Piezas: ${this.piezas[index] || 0}`,
        `Peso: ${this.peso || 0} kg`,
        `Total: ${this.totalPiezas}`,
        `Paquetería: ${this.paqueteriaSeleccionada.nombre || '-'}`,
        `Embalaje: ${this.tipoEmbalaje || '-'}`,
        `Clave: ${this.claveProducto || '-'}`,
      ];
      if (this.paqueteriaSeleccionada.nombre === "Estafeta") {
        data.push(`Ancho: ${this.anchoCaja || 0} cm`);
        data.push(`Alto: ${this.altoCaja || 0} cm`);
        data.push(`Largo: ${this.largoCaja || 0} cm`);
        this.piezas.forEach((p, i) => data.push(`Caja ${i+1} Piezas: ${p}`));
      }
      return data.join("\n");
    },
    imprimirZebra() {
      this.imprimir();
    },
    imprimir() {
      if (!this.numCajas || this.numCajas <= 0) return alert("No hay etiquetas para imprimir");
      this.$nextTick(() => setTimeout(() => window.print(), 200));
    },
    async imprimirRemoto() {
      if (!this.numCajas) return alert("No hay etiquetas para imprimir");
      try {
        for (let i = 0; i < this.numCajas; i++) {
          const zpl = this.generateZPL(i);
          await axios.post("http://127.0.0.1:8000/print_label/", { zpl });
        }
        alert("Todas las etiquetas fueron enviadas al servidor en formato ZPL");
      } catch (error) {
        console.error(error);
        alert("Error al enviar etiquetas ZPL al servidor");
      }
    },
    generateZPL(index) {
      return `^XA
^FO50,50^ADN,36,20^FDFactura: ${this.factura || '-'}^FS
^FO50,100^ADN,36,20^FDCaja: ${index + 1} de ${this.numCajas}^FS
^FO50,150^ADN,36,20^FDPiezas: ${this.piezas[index] || 0}^FS
^FO50,200^ADN,36,20^FDPeso: ${this.peso || 0} kg^FS
^FO50,250^ADN,36,20^FDTotal: ${this.totalPiezas}^FS
^FO50,300^ADN,36,20^FDPaquetería: ${this.paqueteriaSeleccionada.nombre || '-'}^FS
^FO50,350^ADN,36,20^FDEmbalaje: ${this.tipoEmbalaje || '-'}^FS
^FO50,400^ADN,36,20^FDClave: ${this.claveProducto || '-'}^FS
^FO50,450^BQN,2,5^FDLA,${this.generateQR(index)}^FS
^XZ`;
    },
    reiniciar() {
      this.factura = "";
      this.numCajas = 0;
      this.piezas = [];
      this.paqueteriaSeleccionada = { nombre: "", logo: "" };
      this.tipoEmbalaje = 1;
      this.claveProducto = "";
      this.anchoCaja = "";
      this.altoCaja = "";
      this.largoCaja = "";
      this.peso = "";
    },
    async guardarDatosPracticante() {
      if (!this.factura || !this.tipoEmbalaje || !this.paqueteriaSeleccionada.nombre || !this.claveProducto) {
        return alert("Completa todos los campos obligatorios");
      }

      try {
        const payload = {
          paqueteria: String(this.paqueteriaSeleccionada.nombre),
          numero_factura: String(this.factura),
          numero_cajas: Number(this.numCajas) || 0,
          tipo_embalaje: String(this.tipoEmbalaje),
          cantidad_piezas: this.piezas.reduce((acc, val) => acc + (Number(val) || 0), 0),
          clave_producto: String(this.claveProducto),
          ancho: Number(this.anchoCaja) || 0,
          alto: Number(this.altoCaja) || 0,
          largo: Number(this.largoCaja) || 0,
          peso: Number(this.peso) || 0
        };

        console.log("Payload enviado:", JSON.stringify(payload, null, 2));

        const token = localStorage.getItem("token");
        const response = await fetch("http://127.0.0.1:8000/cajas/?role=practicante", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(token ? { token } : {})
          },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Error en API:", errorData);
          alert("Error en API: " + JSON.stringify(errorData, null, 2));
          throw new Error("Error al guardar en la base de datos");
        }

        alert("✅ Datos guardados correctamente");
        this.reiniciar();
      } catch (err) {
        console.error(err);
        alert("Ocurrió un error al guardar los datos");
      }
    },
    async checkPrinterStatus() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/print_label/status");
        this.impresoraOnline = res.data.online;
      } catch {
        this.impresoraOnline = false;
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

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
  background: linear-gradient(to right, #031021, #0b22a1);
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
