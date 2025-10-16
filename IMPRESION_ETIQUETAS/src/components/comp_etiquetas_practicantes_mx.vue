<!-- src/components/CompEtiquetasPracticantes.vue -->
<template>
  <div class="app-container">
    <!-- BARRA SUPERIOR -->
    <header class="header no-print">
      <div class="header-content">
        <h1 class="logo">
          <i class="fas fa-box"></i> Proceso de Embalaje <span class="green-dot">MX</span>
        </h1>
        <h2 class="coordinador-title">
          <i class="fas fa-user-graduate"></i> Practicante
        </h2>
        <div class="user-info">
          🕖 Entrada: <strong v-if="horaEntrada">{{ horaEntrada }}</strong> |
          Mesa: <strong v-if="mesa_trabajo">{{ mesa_trabajo }}</strong> |
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
    <h3 class="modal-title">
      <i class="fas fa-user-edit"></i> Editar Perfil
    </h3>

    <div class="form-field">
      <label class="crud-label">Nombre</label>
      <input v-model="editUser.nombre" class="crud-input" placeholder="Nombre completo" />
    </div>

    <div class="form-field">
    <label class="crud-label">Mesa de trabajo</label>
    <select v-model="editUser.mesa_trabajo" class="crud-input" required>
      <option disabled value="">Selecciona la mesa</option>
      <option v-for="n in 10" :key="n" :value="`MESA${n}`">MESA{{ n }}</option>
    </select>
  </div>


    <div class="form-field">
      <label class="crud-label">Contraseña</label>
      <input v-model="editUser.contrasena" type="password" class="crud-input" placeholder="Nueva contraseña" />
    </div>

    

    <div class="crud-actions centered">
      <button @click="saveUser" class="btn btn-save">
        <i class="fas fa-save"></i> Guardar Cambios
      </button>
      <button @click="closeEditUserModal" class="btn btn-reset">
        <i class="fas fa-times"></i> Cancelar
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
            <!-- FORMULARIO REORGANIZADO -->
            <div class="etiquetas-container">
              <!-- FILA 1: Datos generales -->
              <div class="fila-general">
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
              </div>

              <!-- FILA 2: Dimensiones y peso -->
              <div class="fila-dimensiones" v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'">
                <div class="form-field">
                  <label class="crud-label">Ancho de la Caja (cm)</label>
                  <input v-model.number="anchoCaja" type="number" min="0" class="crud-input" placeholder="Ej: 40" />
                </div>
                <div class="form-field">
                  <label class="crud-label">Alto de la Caja (cm)</label>
                  <input v-model.number="altoCaja" type="number" min="0" class="crud-input" placeholder="Ej: 60" />
                </div>
                <div class="form-field">
                  <label class="crud-label">Largo de la Caja (cm)</label>
                  <input v-model.number="largoCaja" type="number" min="0" class="crud-input" placeholder="Ej: 50" />
                </div>
                <div class="form-field">
                  <label class="crud-label">Peso (kg)</label>
                  <input v-model.number="peso" type="number" min="0" step="0.01" class="crud-input" placeholder="Ej: 2.5" />
                </div>
                <div class="form-field">
                  <label class="crud-label">Peso Volumétrico (kg)</label>
                  <input :value="pesoVolumetrico.toFixed(2)" type="number" class="crud-input" disabled />
                </div>
              </div>
            </div>

            <!-- PIEZAS Y BOTONES -->
            <div v-if="numCajas > 0" class="mb-4">
              <h3 class="crud-subtitle">Piezas por Caja</h3>
              <div class="pieces-grid">
                <div v-for="n in numCajas" :key="n" class="piece-card">
                  <label class="crud-label-inline">Caja {{ n }}</label>
                  <input v-model.number="piezas[n-1]" type="number" min="0" class="crud-input-small" placeholder="0" />
                </div>
              </div>
            </div>

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
                    <div class="dato"><strong>Mesa:</strong> {{ numMesa || '—' }}</div>
                    <div class="dato"><strong>Caja:</strong> {{ n }} de {{ numCajas }}</div>
                    <div class="dato"><strong>Piezas:</strong> {{ piezas[n-1] || 0 }}</div>
                    <div class="dato"><strong>Peso:</strong> {{ peso || 0 }} kg</div>
                    <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'">
                      <div class="dato"><strong>Ancho:</strong> {{ anchoCaja || 0 }} cm</div>
                      <div class="dato"><strong>Alto:</strong> {{ altoCaja || 0 }} cm</div>
                      <div class="dato"><strong>Largo:</strong> {{ largoCaja || 0 }} cm</div>
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

        <!-- TARIMA -->
        <section v-if="currentView === 'tarima'"><comp_tarima_mx /></section>

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
import comp_tarima_mx from "@/components/comp_tarima_mx.vue";
import comp_inf from "@/components/comp_inf.vue";
import comp_otras_etiquetas from "./comp_otras_etiquetas.vue";

export default {
  name: "CompEtiquetasPracticantes",
  components: { QrcodeVue, comp_tarima_mx, comp_inf, comp_otras_etiquetas },
  data() {
    return {
      username: localStorage.getItem("username") || "",
      horaEntrada: localStorage.getItem("horaEntrada") || "",
      currentView: "caja",
      showEditUserModal: false,
      mesa_trabajo: localStorage.getItem("mesa_trabajo") || "", 
      editUser: {     practicanteId: null,nombre: "", contrasena: "" , mesa_trabajo: "" },
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
      peso: 0,
      qrSize: 130,
    };
  },
  created() {
    this.getUserInfo();
    if (!this.horaEntrada) {
      const hora = new Date().toLocaleString();
      localStorage.setItem("horaEntrada", hora);
      this.horaEntrada = hora;
      this.cargarDatosPracticante();

    }
  },
  computed: {
    totalPiezas() { return this.piezas.reduce((acc, val) => acc + (Number(val) || 0), 0); },
    pesoVolumetrico() { return ((this.anchoCaja * this.altoCaja * this.largoCaja) / 5000) || 0; }
  },
  methods: {
    logout() { localStorage.clear(); this.$router.push("/"); },
    setView(view) { this.currentView = view; },
async cargarDatosPracticante() {
    try {
      const token = localStorage.getItem("token");
      if (!token) return;

      const response = await axios.get("http://127.0.0.1:8000/user_practicantes_mx/me", {
        headers: { Authorization: `Bearer ${token}` }
      });

      const user = response.data;

      this.username = user.nombre || this.username;
      this.mesa_trabajo = user.mesa_trabajo || "";
      localStorage.setItem("mesa_trabajo", this.mesa_trabajo);
      localStorage.setItem("nombre_practicante", this.username);

    } catch (error) {
      console.error("Error al cargar datos del practicante:", error);
    }
  },
async openEditUserModal() {
  try {
    const token = localStorage.getItem("token");
    if (!token) throw new Error("No se encontró token");

    const response = await axios.get("http://127.0.0.1:8000/user_practicantes_mx/me", {
      headers: { Authorization: `Bearer ${token}` }
    });

    const user = response.data;

    this.practicanteId = user.id;  // <-- Guardamos el ID
    this.editUser.nombre = user.nombre || "";
    this.editUser.mesa_trabajo = user.mesa_trabajo || "";

     // 🔹 Actualizamos el header y localStorage
    this.mesa_trabajo = this.editUser.mesa_trabajo;
    localStorage.setItem("mesa_trabajo", this.mesa_trabajo);
    
    this.editUser.contrasena = "";
    this.showEditUserModal = true;

  } catch (error) {
    console.error("Error al cargar los datos del usuario:", error);
    alert("Error al cargar los datos del usuario");
  }
},
    closeEditUserModal() { this.showEditUserModal = false; },
async saveUser() {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("No se encontró el token de autenticación");
      return;
    }

    // Ejecutar actualización
    await axios.put(
      `http://127.0.0.1:8000/user_practicantes_mx/${this.practicanteId}`,
      {
        nombre: this.editUser.nombre || undefined,
        mesa_trabajo: this.editUser.mesa_trabajo || undefined,
        contrasena: this.editUser.contrasena || undefined,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    // 🔹 Actualizamos datos locales para reflejar los cambios inmediatos
    this.username = this.editUser.nombre;
    this.mesa_trabajo = this.editUser.mesa_trabajo;

    localStorage.setItem("username", this.username);
    localStorage.setItem("mesa_trabajo", this.mesa_trabajo);

    // 🔹 Volvemos a cargar la info del usuario desde el backend
    await this.cargarDatosPracticante();

    alert("✅ Perfil actualizado correctamente");
    this.showEditUserModal = false;
  } catch (error) {
    console.error("Error al actualizar el perfil:", error.response || error);
    alert("❌ Ocurrió un error al actualizar el perfil");
  }
},
    reiniciar() {
      this.factura = "";
      this.numCajas = 0;
      this.piezas = [];
      this.paqueteriaSeleccionada = { nombre: "", logo: "" };
      this.tipoEmbalaje = "";
      this.claveProducto = "";
      this.anchoCaja = "";
      this.altoCaja = "";
      this.largoCaja = "";
      this.peso = 0;
    },
    generateQR(index) {
      return JSON.stringify({ factura: this.factura, caja: index + 1, piezas: this.piezas[index] || 0, peso: this.peso, mesa: this.numMesa });
    },
    async imprimirZebra() { alert("Función de impresión en Zebra"); },
    async imprimirRemoto() { alert("Función de impresión en servidor (ZPL)"); },
async guardarDatosPracticante() {
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
  const nombreCoordinador = localStorage.getItem("nombre_coordinador") || this.nombreCoordinador || "Meli";

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
      "http://127.0.0.1:8000/cajas_mx/?sede=mexico&role=practicante",
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
},
    async getUserInfo() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/user_practicantes_mx/me", {  headers: { Authorization: `Bearer ${token}` } });
        if (response.data) {
          this.username = response.data.username || this.username;
          this.numMesa = response.data.mesa_trabajo || this.numMesa;
          localStorage.setItem("username", this.username);
          localStorage.setItem("numMesa", this.numMesa);
        }
        console.log(response.data);
      } catch (err) {
        console.error("Error al obtener info del usuario:", err);
      }
    }
  }
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
  --bg: #f4f7ff;
  --card: #ffffff;
  --muted: #6b7280;
  --primary-dark: #131a2e;
  --primary: #4274c4;
  --secondary: #f97316; /* Naranja Coordinador */
  --accent: #facc15;
  --text: #111827;
  --field-bg: #f9fafb;
  --shadow-light: rgba(0,0,0,0.08);
  --shadow-dark: rgba(0,0,0,0.16);
}

/* ==== GENERAL LAYOUT ==== */
.app-container {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  flex-direction: column;
  font-family: 'Poppins', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color: var(--text);
}
.layout { display: flex; flex:1; margin-top: 60px; }

/* ==== HEADER ==== */
.header {
  background: linear-gradient(to right, #031021, #0b22a1);
  color: #ffffff;
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
.logo { font-size: 1.4rem; font-weight: bold; display: flex; align-items: center; gap: 8px; }
.coordinador-title { font-size: 1.5rem; font-weight: 700; color: #ef4444; display: flex; align-items: center; gap: 8px; margin: 0; }
.user-info { font-weight: bold; font-size: 0.95rem; color: white; display: flex; align-items: center; gap: 10px; }
.btn-logout { background: #c6c4c4; color: #060b14; border: none; padding: 4px 10px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 4px; }
.btn-logout:hover { background: #b0adad; }

/* ==== SIDEBAR ==== */
.sidebar {
  width: 220px;
  background: #1e293b;
  color: white;
  padding-top: 20px;
  min-height: calc(100vh - 60px);
}
.menu ul { list-style: none; padding: 0; margin: 0; padding-top: 20px; }
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
.sidebar-user { display: flex; align-items: center; gap: 8px; padding: 12px 20px; margin-bottom: 20px; cursor: pointer; font-weight: 600; }

/* ==== CONTENT ==== */
.content { flex: 1; padding: 20px; background: var(--bg); }

/* ==== FORM GRID ==== */
.form-grid, .etiquetas-container, .fila-general, .fila-dimensiones {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}
.form-field {
  background: var(--field-bg);
  border-radius: 16px;
  padding: 14px 18px;
  box-shadow: 4px 4px 10px var(--shadow-light), -4px -4px 10px #ffffff;
  transition: all 0.25s ease-in-out;
}
.form-field:hover { box-shadow: 6px 6px 16px var(--shadow-light), -6px -6px 16px #ffffff; }
.crud-label { font-weight: 600; margin-bottom: 8px; display: block; color: #1e3a8a; }
.crud-input, select.crud-input {
  border: none;
  border-radius: 12px;
  width: 100%;
  padding: 10px;
  font-size: 0.95rem;
  background: #f9f9ff;
  box-shadow: inset 2px 2px 6px var(--shadow-light), inset -2px -2px 6px #ffffff;
  transition: all 0.25s ease-in-out;
}
.crud-input:focus, select.crud-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.3);
  background: #ededed;
}

/* ==== PIEZAS POR CAJA ==== */
.pieces-grid { display: flex; flex-wrap: wrap; gap: 14px; }
.piece-card {
  background: #feebe0;
  border-radius: 14px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 90px;
  box-shadow: 4px 4px 10px var(--shadow-light), -4px -4px 10px #ffffff;
  transition: all 0.25s ease-in-out;
}
.piece-card:hover { transform: translateY(-2px); box-shadow: 6px 6px 16px var(--shadow-light), -6px -6px 16px #ffffff; background: #bae6fd; }
.crud-label-inline { font-weight: 600; margin-bottom: 6px; text-align: center; }
.crud-input-small { border: none; border-radius: 8px; width: 60px; padding: 6px; font-size: 0.9rem; text-align: center; background: #f9f9ff; box-shadow: inset 2px 2px 6px var(--shadow-light), inset -2px -2px 6px #ffffff; }

/* ==== CRUD CARD ==== */
.crud-card {
  background: var(--card);
  border-radius: 20px;
  padding: 26px;
  box-shadow: 12px 12px 24px var(--shadow-light), -12px -12px 24px #ffffff;
  transition: all 0.3s ease-in-out;
}
.crud-card:hover { transform: translateY(-3px); box-shadow: 16px 16px 32px var(--shadow-light), -16px -16px 32px #ffffff; }
.crud-subtitle { font-size: 28px; font-weight: 700; color: #1f618d; margin-bottom: 20px; border-left: 6px solid #2980b9; padding-left: 12px; }

/* ==== BOTONES ==== */
.crud-actions.centered { display: flex; justify-content: center; flex-wrap: wrap; gap: 12px; margin-top: 20px; }
.btn {
  padding: 12px 22px;
  font-weight: 600;
  border-radius: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.95rem;
  transition: all 0.25s ease-in-out;
  box-shadow: 6px 6px 12px var(--shadow-light), -6px -6px 12px #ffffff;
  border: none;
}
.btn:hover { transform: translateY(-2px); box-shadow: 8px 8px 16px var(--shadow-light), -8px -8px 16px #ffffff; }
.btn-print { background: linear-gradient(135deg, #22c55e, #16a34a); color: #fff; }
.btn-reset { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #fff; }
.btn-save { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: #fff; }

/* ==== ETIQUETAS ==== */
.labels-container { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 24px; width: 100%; }
.etiqueta {
  background: var(--card);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 12px 12px 24px var(--shadow-light), -12px -12px 24px #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  min-width: 160px;
  text-align: center;
}
.etiqueta h3 { font-size: 1.1rem; font-weight: 700; color: #1e40af; margin: 0; }
.etiqueta p { font-size: 0.9rem; color: var(--muted); margin: 0; }
.etiqueta canvas { margin-top: 6px; }

/* ==== RESPONSIVE ==== */
@media (max-width: 1024px) {
  .layout { flex-direction: column; }
  .sidebar { width: 100%; min-height: auto; }
  .content { padding: 12px; }
  .form-grid, .etiquetas-container { grid-template-columns: 1fr; }
}


/* ==== MODAL ==== */
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  animation: fadeIn 0.25s ease-in-out;
}

.modal-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px 34px;
  width: 90%;
  max-width: 420px;
  box-shadow: 0 12px 30px rgba(0,0,0,0.25);
  animation: slideUp 0.3s ease-in-out;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Animaciones suaves */
@keyframes fadeIn {
  from { opacity: 0; } to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(40px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}



</style>


