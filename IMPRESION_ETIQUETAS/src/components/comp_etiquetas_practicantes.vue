<!-- src/components/CompEtiquetas.vue -->
<template>
  <div class="app-container">
    <!-- BARRA SUPERIOR -->
    <header class="header no-print">
      <div class="header-content">
        <h1 class="logo">📦 Proceso de Embalaje</h1>
        <div class="user-info"> 🚹
          {{ username }} |
          <strong v-if="mesaSeleccionada">💻 Mesa de trabajo: {{ mesaSeleccionada }}</strong> |
          🕖 Entrada: <strong v-if="horaEntrada">{{ horaEntrada }}</strong> |
          <button class="btn-logout" @click="logout">Salir</button>
        </div>
      </div>
    </header>

    <!-- LAYOUT -->
    <div class="layout">
      <!-- SIDEBAR -->
      <aside class="sidebar no-print">
        <nav class="menu">
          <ul>
            <h2>  Practicante</h2>
            <li :class="{active: currentView === 'caja'}" @click="setView('caja')">📦 Etiquetas por Caja</li>
            <li :class="{active: currentView === 'tarima'}" @click="setView('tarima')">📦 Etiquetas por Tarima</li>
            <li :class="{active: currentView === 'otrasetiquetas'}" @click="setView('otras_etiquetas')"> ⚠️  Otras Etiquetas</li>
            <li :class="{active: currentView === 'info'}" @click="setView('info')">💻 Acerca de . . .</li>
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

              <!-- 🔹 SOLO SI ES ESTAFETA -->
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

            <!-- 🔹 ESTATUS DE IMPRESORA -->
            <div class="printer-status no-print">
              🖨️ Estado de Impresora:
              <span :class="{ online: impresoraOnline, offline: !impresoraOnline }">
                {{ impresoraOnline ? "En línea ✅" : "Desconectada ❌" }}
              </span>
            </div>

            <div class="crud-actions no-print">
            <button @click="imprimirZebra" class="btn btn-print">🖨️ Imprimir en Zebra</button>
              <button @click="imprimirRemoto" class="btn btn-print">🌐 Imprimir en Servidor (ZPL)</button>
              <button @click="reiniciar" class="btn btn-reset">🔄 Reiniciar</button>
              <button @click="guardarDatos" class="btn btn-save">💾 Guardar</button>
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

                    <!-- 🔹 Medidas solo si es Estafeta -->
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
        <section v-if="currentView === 'tarima'">
          <comp_tarima />
        </section>

        <!-- OTRAS ETIQUETAS -->
        <section v-if="currentView === 'otras_etiquetas'">
          <comp_otras_etiquetas />
        </section>

        <!-- INFO -->
        <section v-if="currentView === 'info'">
          <comp_inf />
        </section>
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
  name: "CompEtiquetas",
  components: { QrcodeVue, comp_tarima, comp_inf, comp_otras_etiquetas },
  data() {
    return {
      username: localStorage.getItem("username") || "",
      mesaSeleccionada: localStorage.getItem("mesaSeleccionada") || "",
      horaEntrada: "",
      currentView: "caja",
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
      qrSize: 130,
      impresoraOnline: false,
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
    },
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/');
    },
    setView(view) {
      this.currentView = view;
    },
    generateQR(index) {
      let data = [
        `Factura: ${this.factura || '-'}`,
        `Caja: ${index + 1} de ${this.numCajas || 0}`,
        `Piezas: ${this.piezas[index] || 0}`,
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
    imprimir() {
      if (!this.numCajas || this.numCajas <= 0) return alert("No hay etiquetas para imprimir");
      this.$nextTick(() => setTimeout(() => window.print(), 200));
    },
    async imprimirRemoto() {
      if (!this.numCajas) return alert("No hay etiquetas para imprimir");
      try {
        for (let i = 0; i < this.numCajas; i++) {
          // Genera ZPL para cada etiqueta
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
      // Formato ZPL básico
      return `
^XA
^FO50,50^ADN,36,20^FDFactura: ${this.factura || '-'}^FS
^FO50,100^ADN,36,20^FDCaja: ${index + 1} de ${this.numCajas}^FS
^FO50,150^ADN,36,20^FDPiezas: ${this.piezas[index] || 0}^FS
^FO50,200^ADN,36,20^FDTotal: ${this.totalPiezas}^FS
^FO50,250^ADN,36,20^FDPaquetería: ${this.paqueteriaSeleccionada.nombre || '-'}^FS
^FO50,300^ADN,36,20^FDEmbalaje: ${this.tipoEmbalaje || '-'}^FS
^FO50,350^ADN,36,20^FDClave: ${this.claveProducto || '-'}^FS
^FO50,400^BQN,2,5^FDLA,${this.generateQR(index)}^FS
^XZ
      `;
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
    },
    async guardarDatos() {
      if (!this.factura || !this.paqueteriaSeleccionada.nombre || !this.tipoEmbalaje || !this.numCajas) {
        return alert("Factura, Paquetería, Tipo de Embalaje y Número de Cajas son obligatorios");
      }
      try {
        const payload = {
          paqueteria: this.paqueteriaSeleccionada.nombre,
          numero_factura: this.factura,
          numero_cajas: Number(this.numCajas),
          tipo_embalaje: Number(this.tipoEmbalaje),
          cantidad_piezas: this.totalPiezas,
          clave_producto: this.claveProducto || "N/A",
          ancho: Number(this.anchoCaja || 0),
          alto: Number(this.altoCaja || 0),
          largo: Number(this.largoCaja || 0),
        };
        await fetch('http://127.0.0.1:8000/cajas/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        alert("Datos guardados correctamente");
        this.reiniciar();
      } catch (err) {
        console.error(err);
        alert("Error al guardar");
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
/* ==== LAYOUT GENERAL ==== */
.app-container { min-height: 100vh; background: #f9fafb; display: flex; flex-direction: column; }
.layout { display: flex; flex: 1; margin-top: 60px; }

/* BARRA SUPERIOR */
.header { background: linear-gradient(to right, #131a2e, #4274c4); color: rgb(196, 205, 217); position: fixed; top: 0; left: 0; right: 0; z-index: 100; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
.header-content { max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; }
.logo { font-size: 1.2rem; font-weight: bold; }
.user-info { font-weight: bold; font-size: 0.95rem; color: white; display: flex; align-items: center; gap: 10px; }
.btn-logout { background: #c6c4c4; color: rgb(6, 11, 20); border: none; padding: 4px 10px; border-radius: 6px; cursor: pointer; }

/* SIDEBAR */
.sidebar { width: 220px; background: #1e293b; color: white; padding-top: 20px; min-height: calc(100vh - 60px); }
.menu ul { list-style: none; padding: 0; margin: 0; }
.menu li { padding: 12px 20px; cursor: pointer; font-weight: 500; border-left: 4px solid transparent; }
.menu li:hover { background: #334155; }
.menu li.active { background: #3567b6; border-left: 4px solid #facc15; }

/* CONTENIDO */
.content { flex: 1; padding: 20px; background: #f9fafb; }

/* FORMULARIO MODERNO */
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 20px; }
.form-field { background: #f9fafb; border-radius: 12px; padding: 14px 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); transition: all 0.2s; }
.form-field:hover { box-shadow: 0 6px 18px rgba(0,0,0,0.12); }
.crud-label { font-weight: 600; margin-bottom: 8px; display: block; color: #1e3a8a; }
.crud-input { border: 1px solid #d1d5db; border-radius: 8px; width: 100%; padding: 10px; font-size: 0.95rem; transition: all 0.2s; }
.crud-input:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 5px rgba(37, 99, 235, 0.3); }

/* PIEZAS POR CAJA */
.pieces-grid { display: flex; flex-wrap: wrap; gap: 14px; }
.piece-card { background: #e0f2fe; border-radius: 10px; padding: 10px 14px; display: flex; flex-direction: column; align-items: center; min-width: 90px; transition: all 0.2s; }
.piece-card:hover { background: #bae6fd; }
.crud-label-inline { font-weight: 600; margin-bottom: 6px; text-align: center; }
.crud-input-small { border: 1px solid #9ca3af; border-radius: 6px; width: 60px; padding: 6px; font-size: 0.9rem; text-align: center; }

/* CRUD GENERAL */
.crud-card { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
.crud-subtitle { font-weight: 600; margin-bottom: 12px; color: #1e40af; font-size: 1.05rem; }
.crud-actions { display: flex; gap: 12px; margin-top: 16px; }
.btn { padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
.btn-print { background: #126330; color: white; }
.btn-reset { background: #cd981c; color: white; }
.btn-save { background: #2559ac; color: white; }

/* ETIQUETAS */
.labels-container { display: flex; flex-wrap: wrap; gap: 16px; margin-top: 20px; width: 100%; }
.etiqueta { 
  background: #ffffff; 
  border-radius: 10px; 
  padding: 14px; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.08); 
  page-break-inside: avoid;
  width: 100%;   
}
.etiqueta-content { 
  display: flex; 
  justify-content: flex-start; /* 🔹 de space-between a flex-start */
  align-items: center; 
  gap: 50px; /* 🔹 controlamos la distancia entre datos y QR */
}
.logo-etiqueta { width: 120px; margin-bottom: 8px; }
.etiqueta-datos { font-size: 1rem; }
.etiqueta-datos .dato { margin-bottom: 12px; }
.etiqueta-qr { margin-left:0px; }

.printer-status {
  background: #f3f4f6;
  color: #111827;
  font-weight: bold;
  text-align: center;
  padding: 8px;
  border-bottom: 2px solid #e5e7eb;
}

.online {
  color: #22c55e;
  font-weight: bold;
}

.offline {
  color: #ef4444;
  font-weight: bold;
}


/* ===== ESTILOS DE IMPRESIÓN ===== */
@media print {
  @page { size: auto; margin: 0; }

  body { background: none !important; }
  body * { visibility: hidden; background: none !important; box-shadow: none !important; }

  .labels-container, .labels-container * { 
    visibility: visible; 
    background: none !important; 
    box-shadow: none !important; 
    color: black !important;
  }

  .labels-container { 
    position: absolute; 
    top: 0; left: 0; 
    width: 100%;  
  }

  .etiqueta { 
    display: block; 
    margin: 0; 
    width: 100%; 
    background: none !important; 
    box-shadow: none !important;
  }  

  .no-print { display: none !important; }
}



</style>
