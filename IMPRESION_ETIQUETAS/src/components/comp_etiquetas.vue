<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Barra superior -->
    <header class="header" v-if="username">
      <div class="header-content">
        <h1 class="logo">📦 Generador de Etiquetas</h1>
        <div class="user-info">
          Hola, {{ username }}!
          <button class="btn-logout" @click="logout">Cerrar sesión</button>
        </div>
      </div>
    </header>

    <!-- Login -->
    <div v-if="!username" class="login-card">
      <h2>Iniciar sesión</h2>
      <input v-model="loginName" type="text" placeholder="Nombre de usuario" class="login-input" />
      <button @click="login" class="btn btn-login">Entrar</button>
    </div>

    <!-- CRUD -->
    <div v-else class="crud-card">
      <div class="mb-3">
        <label class="crud-label">Número de Factura:</label>
        <input v-model="factura" type="text" class="crud-input" placeholder="Factura" />
      </div>

      <div class="mb-3">
        <label class="crud-label">Número de Cajas:</label>
        <input v-model.number="numCajas" type="number" min="0" class="crud-input" placeholder="Ej: 3" />
      </div>

      <div class="mb-3">
        <label class="crud-label">Tamaño de Etiqueta:</label>
        <select v-model="medidaEtiqueta" class="crud-input">
          <option value="pequeña">Pequeña</option>
          <option value="mediana">Mediana</option>
          <option value="grande">Grande</option>
        </select>
      </div>

      <!-- Selección de Paquetería -->
      <div class="nav-crud">
        <button
          v-for="paq in paqueterias"
          :key="paq.nombre"
          class="paq-btn"
          :class="{ 'paq-btn-active': paqueteriaSeleccionada === paq }"
          @click="paqueteriaSeleccionada = paq"
        >
          {{ paq.nombre }}
        </button>
      </div>

      <!-- Piezas por caja -->
      <div v-if="numCajas > 0" class="mb-4">
        <h2 class="crud-subtitle">Piezas por Caja:</h2>
        <div v-for="(caja, index) in numCajas" :key="index" class="crud-row">
          <label class="crud-label-inline">Caja {{ index + 1 }}:</label>
          <input v-model.number="piezas[index]" type="number" min="0" class="crud-input-small" placeholder="0" />
        </div>
      </div>

      <div class="crud-total">
        Total de piezas: {{ totalPiezas }}
      </div>

      <div class="crud-actions">
        <button @click="imprimir" class="btn btn-print">🖨️ Imprimir</button>
        <button @click="reiniciar" class="btn btn-reset">🔄 Reiniciar</button>
      </div>
    </div>

    <!-- Etiquetas -->
    <div class="labels-container">
      <div
        v-for="(caja, index) in numCajas"
        :key="'etiqueta-' + index"
        class="etiqueta"
        :class="medidaEtiqueta"
      >
        <div class="contenido">
          <div class="logo-wrapper">
            <img :src="paqueteriaSeleccionada.logo" :alt="paqueteriaSeleccionada.nombre + ' Logo'" class="logo-etiqueta" />
          </div>

          <div class="etiqueta-content">
            <div class="etiqueta-datos">
              <div class="dato"><strong>Factura:</strong> {{ factura || '—' }}</div>
              <div class="dato"><strong>Caja:</strong> {{ index + 1 }} de {{ numCajas }}</div>
              <div class="dato"><strong>Piezas:</strong> {{ piezas[index] || 0 }}</div>
            </div>

            <div class="etiqueta-qr">
              <qrcode-vue :value="generateQR(index)" :size="qrSize" level="H" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from "vue";
import QrcodeVue from "qrcode.vue";

const loginName = ref("");
const username = ref(localStorage.getItem("username") || null);

const factura = ref("");
const numCajas = ref(0);
const piezas = ref([]);
const medidaEtiqueta = ref("mediana");

watch(numCajas, (n) => {
  const N = Number(n) || 0;
  if (N > piezas.value.length) {
    for (let i = piezas.value.length; i < N; i++) piezas.value.push(0);
  } else {
    piezas.value.splice(N);
  }
});

const paqueterias = [
  { nombre: "Paquetexpress", logo: new URL("@/assets/pExp.png", import.meta.url).href },
  { nombre: "FedEx", logo: new URL("@/assets/fedex.png", import.meta.url).href },
  { nombre: "DHL", logo: new URL("@/assets/dhl.png", import.meta.url).href },
  { nombre: "Estafeta", logo: new URL("@/assets/estafeta.png", import.meta.url).href },
  { nombre: "Mercado Libre", logo: new URL("@/assets/mercadolibre.png", import.meta.url).href },
  { nombre: "UPS", logo: new URL("@/assets/ups.png", import.meta.url).href },
];

const paqueteriaSeleccionada = ref(paqueterias[0]);

const totalPiezas = computed(() =>
  piezas.value.reduce((acc, val) => acc + (Number(val) || 0), 0)
);

function generateQR(index) {
  return `Factura: ${factura.value || '-'}
Caja: ${index + 1} de ${numCajas.value || 0}
Piezas: ${piezas.value[index] || 0}
Total: ${totalPiezas.value}
Paquetería: ${paqueteriaSeleccionada.value.nombre}
Usuario: ${username.value || '-'}`;
}

const qrSize = computed(() => {
  if (medidaEtiqueta.value === "pequeña") return 80;
  if (medidaEtiqueta.value === "mediana") return 120;
  return 160;
});

async function imprimir() {
  if (!numCajas.value || numCajas.value <= 0) {
    return alert("No hay etiquetas para imprimir");
  }

  await nextTick();
  if (window.BrowserPrint) {
    window.BrowserPrint.getDefaultDevice("printer", function(printer) {
      if (!printer) return alert("No se encontró impresora Zebra.");
      piezas.value.forEach((_, index) => {
        const etiqueta = `
          ^XA
          ^PW800
          ^LL600
          ^FO50,50
          ^A0N,50,50
          ^FDFactura: ${factura.value}^FS
          ^FO50,120
          ^FDCaja: ${index + 1} de ${numCajas.value}^FS
          ^FO50,190
          ^FDPiezas: ${piezas.value[index] || 0}^FS
          ^FO50,260
          ^BQN,2,5
          ^FDLA,${generateQR(index)}^FS
          ^XZ
        `;
        printer.send(etiqueta, undefined, undefined);
      });
    });
  } else {
    setTimeout(() => window.print(), 250);
  }
}

function reiniciar() {
  factura.value = "";
  numCajas.value = 0;
  piezas.value = [];
  medidaEtiqueta.value = "mediana";
}

function login() {
  if (loginName.value.trim()) {
    username.value = loginName.value.trim();
    localStorage.setItem("username", username.value);
  } else {
    alert("Ingresa tu nombre");
  }
}

function logout() {
  username.value = null;
  localStorage.removeItem("username");
  location.reload();
}
</script>

<style scoped>
/* Barra superior */
.header {
  background: linear-gradient(to right, #1e3a8a, #3b82f6);
  color: white;
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 50;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.header-content {
  max-width: 1100px;
  margin: 0 auto;
  display: flex; justify-content: space-between; align-items: center;
  padding: 14px 20px;
}
.logo { font-size: 1.2rem; font-weight: bold; }
.user-info { font-weight: bold; font-size: 1rem; color: white; }
.btn-logout {
  background: #dc2626;
  color: white; border: none; padding: 4px 10px;
  border-radius: 6px; cursor: pointer;
}

.logo-etiqueta {
  max-width: 90%;       /* No más del 30% del ancho de la etiqueta */
  max-height: 60px;     /* Altura máxima */
  object-fit: contain;   /* Mantiene proporción sin deformar */
}


/* Login */
.login-card {
  max-width: 400px;
  margin: 160px auto 20px auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  background: white;
  text-align: center;
}
.login-input { width: 80%; padding: 8px; margin-bottom: 12px; border-radius: 6px; border: 1px solid #ccc; }
.btn-login { background: #2563eb; color: white; border: none; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-weight: 600; }

/* CRUD */
.crud-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  max-width: 450px;
  margin: 140px auto 20px auto;
  padding: 24px;
  border: 1px solid #ddd;
}
.crud-label { font-weight: 600; margin-bottom: 4px; display: block; }
.crud-input { border: 1px solid #ccc; border-radius: 6px; width: 90%; padding: 8px; }
.crud-input-small { border: 1px solid #ccc; border-radius: 6px; width: 60px; padding: 6px; }
.crud-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.crud-label-inline { font-weight: 500; font-size: 0.9rem; }
.crud-subtitle { font-weight: 600; margin-bottom: 6px; }
.crud-total { font-weight: bold; color: #1e3a8a; margin-bottom: 10px; }
.crud-actions { display: flex; gap: 10px; }
.btn { padding: 6px 14px; border-radius: 6px; font-weight: 600; color: white; cursor: pointer; border: none; }
.btn-print { background: #2563eb; }
.btn-reset { background: #2d9752; }

.nav-crud { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; }
.paq-btn { padding: 6px 12px; border-radius: 6px; background: #e0e0e0; color: #111; font-weight: 600; cursor: pointer; }
.paq-btn-active { background: #facc15; }

/* Etiquetas */
.labels-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin: 20px auto;
  padding-bottom: 30px;
}
.etiqueta {
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  page-break-after: always;
  position: relative;

  /* Tamaño para impresión (horizontal) */
  width: 12cm;
  height: 7cm;
}
.etiqueta.pequeña { width: 9cm; height: 6cm; }
.etiqueta.mediana { width: 12cm; height: 7cm; }
.etiqueta.grande { width: 15cm; height: 9cm; }

.contenido {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  transform: rotate(0deg); /* horizontal por defecto */
}

.dato { font-size: 1.2rem; margin-bottom: 4px; }
.etiqueta-qr canvas, .etiqueta-qr svg { max-width: 100px; max-height: 100px; }

@media print {
  @page { size: A4 portrait; margin: 1.5cm; }
  body * { visibility: hidden !important; }
  .labels-container, .labels-container * { visibility: visible !important; }
  .header, .crud-card, .login-card { display: none !important; }
  .labels-container { justify-content: center !important; align-items: center !important; }
  .etiqueta { page-break-after: always !important; border: 2px solid #000; }
}
/* Contenido de la etiqueta - solo en pantalla */
@media screen {
  .etiqueta {
    width: 7cm;   /* ancho menor que alto */
    height: 12cm; /* alto mayor que ancho */
  }

  .contenido {
    transform: rotate(0deg);
    transform-origin: center center;
  }
}

/* En impresión, quitar la rotación */
@media print {
  @page { size: A4 portrait; margin: 1.5cm; }
  body * { visibility: hidden !important; }
  .labels-container, .labels-container * { visibility: visible !important; }
  .header, .crud-card, .login-card { display: none !important; }
  .labels-container { justify-content: center !important; align-items: center !important; }
  .etiqueta { page-break-after: always !important; border: 2px solid #000; }

  /* Contenido horizontal en impresión */
  .contenido {
    transform: rotate(90deg);
  }
}

</style>
