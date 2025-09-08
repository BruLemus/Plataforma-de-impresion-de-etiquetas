<template>
  <div id="app">
    <!-- Barra Superior -->
    <header class="top-bar no-print">
      <h1 class="logo">📦 Generador de Etiquetas</h1>
      <nav class="nav-buttons">
        <button>Paquetexpress</button>
        <button>FedEx</button>
        <button>DHL</button>
        <button>Estafeta</button>
        <button>Mercado Libre</button>
        <button>UPS</button>
      </nav>
    </header>

    <!-- Contenido principal -->
    <main class="content">
      <div class="crud-container">
        <label for="cajas">Número de Cajas:</label>
        <input
          id="cajas"
          type="number"
          v-model="numCajas"
          min="0"
          @input="generarEtiquetas"
        />

        <p>Total de piezas: {{ totalPiezas }}</p>

        <div class="botones">
          <button class="btn imprimir" @click="imprimir">🖨️ Imprimir</button>
          <button class="btn reiniciar" @click="reiniciar">🔄 Reiniciar</button>
        </div>
      </div>

      <!-- Etiquetas -->
      <div class="etiquetas">
        <div
          v-for="(etiqueta, index) in etiquetas"
          :key="index"
          class="etiqueta"
        >
          <p><strong>Etiqueta {{ index + 1 }} de {{ numCajas }}</strong></p>
          <p>Número de piezas: {{ piezasPorCaja }}</p>
          <p>Caja: {{ index + 1 }}</p>
          <img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=Etiqueta-{{index+1}}" alt="QR">
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const numCajas = ref(0);
const piezasPorCaja = ref(10); // ejemplo
const etiquetas = ref([]);

const totalPiezas = computed(() => numCajas.value * piezasPorCaja.value);

const generarEtiquetas = () => {
  etiquetas.value = Array.from({ length: numCajas.value }, (_, i) => i + 1);
};

const imprimir = () => {
  window.print();
};

const reiniciar = () => {
  numCajas.value = 0;
  etiquetas.value = [];
};
</script>

<style>
/* Barra superior */
.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(90deg, #004aad, #5aa0f0);
  color: white;
  display: flex;
  align-items: center;
  padding: 10px 20px;
  z-index: 1000;
  flex-wrap: wrap;
}

.logo {
  flex: 1;
  font-size: 1.4em;
  font-weight: bold;
}

.nav-buttons {
  display: flex;
  gap: 10px;
}

.nav-buttons button {
  background: #f1f1f1;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

.nav-buttons button:hover {
  background: #ddd;
}

/* Contenido principal centrado */
.content {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;  
  justify-content: center; /* Centrado vertical */
  padding-top: 60px; /* espacio por la barra fija */
  box-sizing: border-box;
}

/* CRUD centrado */
.crud-container {
  background: #fff;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  max-width: 350px;
  width: 100%;
  text-align: center;
}

.crud-container input {
  width: 120px;
  padding: 5px;
  margin: 8px 0;
}

.botones {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.btn {
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  border: none;
  color: white;
}

.imprimir {
  background: #007bff;
}

.reiniciar {
  background: #dc3545;
}

/* Etiquetas */
.etiquetas {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

.etiqueta {
  width: 20cm;
  height: 15cm;
  border: 2px dashed #333;
  padding: 20px;
  page-break-after: always; /* Cada etiqueta en hoja nueva */
}

/* Responsivo */
@media (max-width: 768px) {
  .nav-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }

  .crud-container {
    max-width: 90%;
  }
}

/* Ocultar barra al imprimir */
@media print {
  .no-print {
    display: none !important;
  }

  .content {
    justify-content: flex-start; /* Para impresión no centramos */
  }
}
</style>
