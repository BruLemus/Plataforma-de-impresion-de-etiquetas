<template>
  <div class="container">
    <!-- Barra superior -->
    <header class="top-bar">
      <h1>📦 Generador de Etiquetas</h1>
      <nav>
        <button
          v-for="paq in paqueterias"
          :key="paq.nombre"
          @click="seleccionarPaqueteria(paq)"
          :class="{ 'selected': paqueteriaSeleccionada.nombre === paq.nombre }"
        >
          {{ paq.nombre }}
        </button>
      </nav>
    </header>

    <!-- CRUD -->
    <div class="crud-section">
      <div class="input-group">
        <label>Número de Factura:</label>
        <input v-model="factura" type="text" placeholder="Ingresa el número de factura" />
      </div>

      <div class="input-group">
        <label>Número de Cajas:</label>
        <input v-model.number="numCajas" type="number" min="1" placeholder="Ejemplo: 3" />
      </div>

      <div v-if="numCajas > 0" class="input-group">
        <label>Piezas por Caja:</label>
        <div v-for="(caja, index) in numCajas" :key="index" class="caja-row">
          <span>Caja {{ index + 1 }}:</span>
          <input v-model.number="piezas[index]" type="number" min="0" placeholder="0" />
        </div>
      </div>

      <div class="total">
        Total de piezas: {{ totalPiezas }}
      </div>

      <div class="button-group">
        <button class="print-btn" @click="imprimir">🖨️ Imprimir</button>
        <button class="reset-btn" @click="reiniciar">🔄 Reiniciar</button>
      </div>
    </div>

    <!-- Etiquetas -->
    <div class="etiquetas-list">
      <div
        v-for="(caja, index) in numCajas"
        :key="'etiqueta-' + index"
        class="etiqueta-card"
      >
        <div class="logo">
          <img
            :src="paqueteriaSeleccionada.logo"
            :alt="paqueteriaSeleccionada.nombre + ' Logo'"
          />
        </div>

        <div><strong>Factura:</strong> {{ factura }}</div>
        <div><strong>Caja:</strong> {{ index + 1 }} de {{ numCajas }}</div>
        <div><strong>Piezas:</strong> {{ piezas[index] || 0 }}</div>

        <div class="qr">
          <qrcode-vue :value="generateQR(index)" :size="100" level="H" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import QrcodeVue from "qrcode.vue";

const factura = ref("");
const numCajas = ref(0);
const piezas = ref([]);

const paqueterias = [
  { nombre: "Paquetexpress", logo: new URL("@/assets/pExp.png", import.meta.url).href },
  { nombre: "FedEx", logo: new URL("@/assets/fedex.png", import.meta.url).href },
  { nombre: "DHL", logo: new URL("@/assets/dhl.png", import.meta.url).href },
  { nombre: "Estafeta", logo: new URL("@/assets/estafeta.png", import.meta.url).href },
  { nombre: "Mercado Libre", logo: new URL("@/assets/mercadolibre.png", import.meta.url).href },
  { nombre: "UPS", logo: new URL("@/assets/ups.png", import.meta.url).href },
];

const paqueteriaSeleccionada = ref(paqueterias[0]);

function seleccionarPaqueteria(paq) {
  paqueteriaSeleccionada.value = paq;
}

const totalPiezas = computed(() =>
  piezas.value.reduce((acc, val) => acc + (Number(val) || 0), 0)
);

function generateQR(index) {
  return `Factura: ${factura.value}
Caja: ${index + 1} de ${numCajas.value}
Piezas: ${piezas.value[index] || 0}
Total de piezas: ${totalPiezas.value}
Paquetería: ${paqueteriaSeleccionada.value.nombre}`;
}

function imprimir() {
  window.print();
}

function reiniciar() {
  factura.value = "";
  numCajas.value = 0;
  piezas.value = [];
  paqueteriaSeleccionada.value = paqueterias[0];
}
</script>

<style>
/* ====== Estilos generales ====== */
.container {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background: #f0f2f5;
  padding-top: 100px;
  padding-left: 16px;
  padding-right: 16px;
}

.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to right, #1e3a8a, #3b82f6);
  color: white;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  z-index: 10;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.top-bar nav {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.top-bar nav button {
  padding: 6px 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: bold;
  transition: 0.3s;
  font-size: 0.9rem;
}

.top-bar nav button:hover,
.top-bar nav button.selected {
  background: #fde047;
  color: #111;
}

/* CRUD */
.crud-section {
  max-width: 600px;
  width: 100%;
  margin: 0 auto 30px auto;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.input-group input {
  width: 100%;
  max-width: 250px;
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.caja-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.caja-row input {
  flex: 0 0 120px;
}

.total {
  font-weight: bold;
  font-size: 1.1rem;
  color: #2563eb;
  margin-bottom: 10px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}

.print-btn,
.reset-btn {
  flex: 1;
  min-width: 120px;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.print-btn {
  background: #2563eb;
  color: white;
}
.print-btn:hover {
  background: #1d4ed8;
}

.reset-btn {
  background: #ef4444;
  color: white;
}
.reset-btn:hover {
  background: #b91c1c;
}

/* Etiquetas en pantalla */
.etiquetas-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.etiqueta-card {
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  border: 1px solid #ddd;
}

.etiqueta-card .logo img {
  max-width: 80%;
  height: auto;
  margin: 0 auto 10px;
}

/* ====== Estilos de impresión ====== */
@media print {
  @page {
    size: 20cm 15cm;
    margin: 0;
  }

  body {
    margin: 0;
    padding: 0;
  }

  .top-bar,
  .crud-section {
    display: none !important;
  }

  .etiquetas-list {
    display: block;
  }

  .etiqueta-card {
    width: 20cm;
    height: 15cm;
    page-break-after: always;
    box-shadow: none;
    border: 1px solid #000;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .etiqueta-card .logo img {
    max-width: 60%;
  }
}
</style>
