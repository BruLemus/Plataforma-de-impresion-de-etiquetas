<!-- src/components/CompEtiquetas.vue -->
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
      >
        <div class="contenido">
          <div class="logo-wrapper">
            <img :src="paqueteriaSeleccionada.logo" :alt="paqueteriaSeleccionada.nombre + ' Logo'" class="logo-etiqueta" />
          </div>
          <div class="etiqueta-content">
            <div class="etiqueta-datos">
              <div class="dato">
                <strong>Factura:</strong>
                <div class="dato-valor">{{ factura || '—' }}</div>
              </div>
              <div class="dato">
                <strong>Caja:</strong>
                <div class="dato-valor">{{ index + 1 }} de {{ numCajas }}</div>
              </div>
              <div class="dato">
                <strong>Piezas:</strong>
                <div class="dato-valor">{{ piezas[index] || 0 }}</div>
              </div>
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

const qrSize = computed(() => 160);

async function imprimir() {
  if (!numCajas.value || numCajas.value <= 0) {
    return alert("No hay etiquetas para imprimir");
  }
  await nextTick();
  setTimeout(() => window.print(), 250);
}

function reiniciar() {
  factura.value = "";
  numCajas.value = 0;
  piezas.value = [];
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
.btn-logout { background: #dc2626; color: white; border: none; padding: 4px 10px; border-radius: 6px; cursor: pointer; }

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

.labels-container { display: flex; flex-direction: column; align-items: center; gap: 20px; margin: 20px auto; padding-bottom: 30px; }

/* VISTA NORMAL → HORIZONTAL */
.etiqueta {
  width: 15cm;
  height: 10cm;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.logo-wrapper { margin-bottom: 15px; }
.logo-etiqueta { max-width: 98%; height: auto; }
.etiqueta-content { display: flex; justify-content: space-between; align-items: center; width: 100%; gap: 15px; }
.dato { font-size: 1.2rem; margin-bottom: 4px; }
.etiqueta-qr { flex-shrink: 0; }

@media print {
  body * {
    visibility: hidden !important;
  }

  .labels-container, .labels-container * {
    visibility: visible !important;
  }

  .header, .crud-card, .login-card {
    display: none !important;
  }

  /* Contenedor de etiquetas: centrado horizontal, cada etiqueta en su propia etiqueta de la Zebra */
  .labels-container {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important; /* centrado horizontal */
    margin: 0 !important;
    padding: 10 !important;
    width: 100vw !important;
  }

  /* Etiqueta: tamaño real de la Zebra */
  .etiqueta {
    width: 10cm !important;
    height: 15cm !important;
    padding: 0mm !important;
    border: none !important;
    margin: 0 !important; /* ← Solo esta línea para margen */
    background: #fff !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    page-break-after: always !important;
    box-sizing: border-box !important;
    box-shadow: none !important;
    position: relative !important;
    font-size: 15pt !important;
    line-height: 1.2 !important;
    text-align: center !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    font-family: Arial, sans-serif !important;
    color: #000 !important;
    visibility: visible !important;
    overflow: hidden !important;
  }

  
  .etiqueta-content {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 50% !important;
    gap: 2mm !important; /* Espacio entre datos y QR */
  }

    .dato {
    font-size: 15pt !important; /* Título de los datos más grande */
  }

  .etiqueta-datos {
    font-size: 14pt !important; /* Datos más grandes */
  }

   .dato-valor {
    font-size: 14pt !important; /* Valor de los datos más grande */
  }
  .etiqueta-qr {
    margin-top: 0 !important;
    margin-left: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
  }

  .logo-wrapper img {
  margin-top: 0 !important; /* ← Elimina cualquier margen superior */
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
  }

  .logo-etiqueta {
    max-width: 40mm !important;
    height: auto !important;
  }

   .etiqueta.mediana {
    width: 10cm !important; 
    height: 15cm !important;
  }

  .etiqueta-qr canvas,
  .etiqueta-qr svg {
    max-width: 5mm !important; /* QR más pequeño */
    height: auto !important;
  }
}

</style>
