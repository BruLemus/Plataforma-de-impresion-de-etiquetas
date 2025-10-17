<template>
  <div class="crud-card no-print">
    <h2 class="crud-subtitle">Etiquetas por Tarima</h2>

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
        <label class="crud-label">Número de Tarimas</label>
        <input v-model.number="numTarimas" type="number" min="0" class="crud-input" placeholder="Ej: 3" />
      </div>

      <div class="form-field">
        <label class="crud-label">Tipo de Embalaje</label>
        <select v-model="tipoEmbalaje" class="crud-input">
          <option disabled value="">-- Selecciona --</option>
          <option v-for="n in 3" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <div class="form-field">
        <label class="crud-label">Clave de Producto</label>
        <input v-model="claveProducto" type="text" class="crud-input" placeholder="Clave del producto" />
      </div>

      <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'" class="form-field">
        <label class="crud-label">Ancho de la Caja (cm)</label>
        <input v-model.number="ancho" type="number" min="0" class="crud-input" placeholder="Ej: 40" />
      </div>
      <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'" class="form-field">
        <label class="crud-label">Alto de la Caja (cm)</label>
        <input v-model.number="alto" type="number" min="0" class="crud-input" placeholder="Ej: 60" />
      </div>
      <div v-if="paqueteriaSeleccionada.nombre === 'Estafeta' || paqueteriaSeleccionada.nombre === 'Paquetexpress'" class="form-field">
        <label class="crud-label">Largo de la Caja (cm)</label>
        <input v-model.number="largo" type="number" min="0" class="crud-input" placeholder="Ej: 50" />
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

    <div v-if="numTarimas > 0" class="mb-4">
      <h3 class="crud-subtitle">Piezas por Tarima</h3>
      <div class="pieces-grid">
        <div v-for="n in numTarimas" :key="n" class="piece-card">
          <label class="crud-label-inline">Tarima {{ n }}</label>
          <input v-model.number="piezas[n-1]" type="number" min="0" class="crud-input-small" placeholder="0" />
        </div>
      </div>
    </div>
    <div class="crud-total">Total de piezas: {{ totalPiezas }}</div>


    <div class="crud-actions centered no-print">
      <button @click="imprimirZebra" class="btn btn-print">
        <i class="fas fa-print"></i> Imprimir
      </button>

      <button @click="guardarDatos" class="btn btn-save">
        <i class="fas fa-save"></i> Guardar
      </button>
    </div>
  </div>

  <div class="labels-container print-only" v-if="numTarimas > 0">
    <div v-for="n in numTarimas" :key="'etiqueta-tarima-' + n" class="etiqueta">

      <img src="@/assets/fmm.png" alt="Logo FMM" class="logo-fmm" />

      <div class="contenido">
        <div class="logo-wrapper">
          <img :src="paqueteriaSeleccionada.logo" class="logo-etiqueta" />
        </div>

        <div class="etiqueta-content">
          <div class="etiqueta-datos">
            <div class="dato"><strong>Factura:</strong> {{ factura || '—' }}</div>
            <div class="dato"><strong>Tarima:</strong> {{ n }} de {{ numTarimas }}</div>
            <div class="dato"><strong>Piezas:</strong> {{ piezas[n-1] || 0 }}</div>
            
            <div
              v-if="
                paqueteriaSeleccionada.nombre === 'Estafeta' ||
                paqueteriaSeleccionada.nombre === 'Paquetexpress'
              "
            >
              <div class="dato">
                <strong>Dim (ANxALxL):</strong> {{ ancho }}x{{ alto }}x{{ largo }} cm
              </div>
              <div class="dato"><strong>Peso:</strong> {{ peso || 0 }} kg</div>
              <div class="dato">
                <strong>Volumétrico:</strong> {{ pesoVolumetrico.toFixed(2) }} kg
              </div>
            </div>
          </div>
          <div class="etiqueta-qr">
            <qrcode-vue :value="generateQR(n - 1)" :size="100" level="H" />
          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>



<script>
import QrcodeVue from "qrcode.vue";
import axios from "axios";
export default {
  name: "CompEtiquetas",
  components: { QrcodeVue},
  data() {
    return {
      // ... Tu lista de paqueterías original ...
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
      numTarimas: 0, 
      tipoEmbalaje: null,
      claveProducto: "",
      ancho: 0, // Ajustado para unificar con el template
      largo: 0, // Ajustado para unificar con el template
      alto: 0, // Ajustado para unificar con el template
      peso: 0,
      piezas: [],
      nombrePracticante: localStorage.getItem("username") || "Practicante", // Asegurando la variable para el QR
    };
  },
  watch: {
    numTarimas(newVal) {
      this.piezas = Array(newVal).fill(0);
    },
  },
  computed: {
    totalPiezas() {
      return this.piezas.reduce((acc, val) => acc + (Number(val) || 0), 0);
    },
    // 🎯 AJUSTE CLAVE: Ahora chequea la propiedad 'nombre' del objeto
    requiereDimensiones() { 
      return (
        this.paqueteriaSeleccionada.nombre === "Estafeta" ||
        this.paqueteriaSeleccionada.nombre === "Paquetexpress"
      );
    },
    pesoVolumetrico() {
      if (!this.requiereDimensiones) return 0;
      const pv = (this.ancho * this.largo * this.alto) / 5000;
      return isNaN(pv) ? 0 : pv;
    },
  },
methods: {
    reiniciar() {
        this.factura = "";
        this.numTarimas = 0;
        this.paqueteriaSeleccionada = { nombre: "", logo: "" }; // Reiniciamos como objeto
        this.tipoEmbalaje = null;
        this.claveProducto = "";
        this.ancho = 0;
        this.largo = 0;
        this.alto = 0;
        this.peso = 0;
        this.piezas = [];
    },
    
    // Función para guardar datos en la base de datos (NO MODIFICADA)
    async guardarDatos() {
        if (
            !this.factura ||
            !this.tipoEmbalaje ||
            !this.paqueteriaSeleccionada.nombre || // Validar el nombre
            !this.claveProducto ||
            this.numTarimas <= 0 || 
            this.totalPiezas <= 0
        ) {
            return alert("Completa todos los campos obligatorios y la cantidad de piezas.");
        }

        try {
            const token = localStorage.getItem("token");
            const id = localStorage.getItem("id");
            const username = localStorage.getItem("username");
            const sede = localStorage.getItem("sede")
            let role = localStorage.getItem("rol"); 
            role = role?.toLowerCase() || "practicante"; 

            // 🔹 Construcción del payload
            const payload = {
                numero_facturas: this.factura,
                numero_tarimas: Number(this.numTarimas) || 0,
                tipo_embalaje: Number(this.tipoEmbalaje),
                paqueteria: this.paqueteriaSeleccionada.nombre, // Enviar solo el nombre
                clave_producto: this.claveProducto,
                cantidad_piezas: this.totalPiezas,
                ancho: this.requiereDimensiones ? Number(this.ancho) : 0,
                largo: this.requiereDimensiones ? Number(this.largo) : 0,
                alto: this.requiereDimensiones ? Number(this.alto) : 0,
                peso: this.requiereDimensiones ? Number(this.peso) : 0,
                peso_volumetrico: this.requiereDimensiones
                    ? Number(this.pesoVolumetrico.toFixed(2))
                    : 0,
                // Lógica de usuario
                practicante_id: role === "practicante" ? Number(id) : null,
                coordinador_id: role === "coordinador" ? Number(id) : null,
                nombre_user_practicante: role === "practicante" ? username || "" : "",
                nombre_user_coordinador: role === "coordinador" ? username || "" : "",
            };

            const response = await fetch(
                `http://127.0.0.1:8000/tarimas_mx/?sede=${sede}&role=${role}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        token: token,
                    },
                    body: JSON.stringify(payload),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                console.error("Error en API:", data);
                return alert("Error al guardar en la base de datos: " + (data.detail ? JSON.stringify(data.detail) : data));
            }

            alert("✅ Datos guardados correctamente");
            this.reiniciar();
        } catch (err) {
            console.error(err);
            alert("❌ Ocurrió un error al guardar los datos");
        }
    },
    
    // Función para generar el contenido del QR (NO MODIFICADA)
    generateQR(index) { return `Factura:${this.factura || "—"}|Tarima:${index+1}|Practicante:${this.nombrePracticante}`; },
    
    
    // FUNCIÓN CLAVE PARA IMPRIMIR ZEBRA (CORREGIDA Y COMPLETA)
    async imprimirZebra() {
        const centralApiUrl = "http://127.0.0.1:8000/imprimir/generate";
        const localApiUrl = "http://127.0.0.1:8001/print";
        let zplCode = "";
        
        // 1. Validar datos básicos
        if (!this.paqueteriaSeleccionada.nombre || !this.factura || this.numTarimas <= 0 || !this.claveProducto || this.totalPiezas <= 0) {
            alert("Completa todos los campos obligatorios y la cantidad de piezas.");
            return;
        }

        // 2. Construir la lista de datos para enviar a la API CENTRAL (Payload)
        const tarimasAImprimir = [];
        
        for (let i = 0; i < this.numTarimas; i++) {
            tarimasAImprimir.push({
                // Los nombres de propiedad DEBEN coincidir con el modelo Pydantic de FastAPI
                paqueteria: this.paqueteriaSeleccionada.nombre,
                factura: this.factura,
                
                num_cajas: Number(this.numTarimas), 
                caja_actual: i + 1,
                piezas: Number(this.piezas[i]) || 0,
                clave_producto: this.claveProducto, 

                ancho: Number(this.ancho) || 0,
                alto: Number(this.alto) || 0,
                largo: Number(this.largo) || 0,
                peso: Number(this.peso) || 0,
                peso_volumetrico: Number(this.pesoVolumetrico.toFixed(2)) || 0,
                
                qr_data: this.generateQR(i), 
            });
        }
        

        // --- PASO A: PRIMERA LLAMADA (API Central) - Obtener ZPL ---
        try {
            console.log(`Paso A: Solicitando ZPL a: ${centralApiUrl}`);
            const generateResponse = await axios.post(centralApiUrl, tarimasAImprimir);
            
            zplCode = generateResponse.data.zpl_code;
            // Validar que el código ZPL no esté vacío
            if (!zplCode || zplCode.length === 0) throw new Error("La API Central devolvió un código ZPL vacío. Revise la consola del servidor 8000.");
            
            console.log("Paso A completado: ZPL generado.");
            
        } catch (error) {
            console.error("❌ Error al generar ZPL:", error.response?.data?.detail || error.message || error);
            const errorMessage = error.response?.data?.detail || "Revise el servidor FastAPI (8000) por errores de Pydantic o sintaxis.";
            alert(`❌ Error al generar ZPL. ¿Está la API Central (${centralApiUrl}) funcionando?\nDetalle: ${errorMessage}`); 
            return;
        }

        // --- PASO B: SEGUNDA LLAMADA (Micro-servicio Local) - Enviar ZPL a USB ---
        try {
            console.log(`Paso B: Enviando ZPL a servicio local: ${localApiUrl}`);
            const printResponse = await axios.post(localApiUrl, { zpl_code: zplCode });
            
            console.log("✅ Impresión USB exitosa:", printResponse.data);
            alert(`✅ ${this.numTarimas} etiquetas enviadas a la impresora USB. ¡Revisa la Zebra ZT230!`);
            
        } catch (error) {
            console.error("❌ Error al imprimir en servicio local:", error.response?.data?.detail || error.message || error);
            alert(`❌ Error de impresión local. Asegúrate de que el **Micro-servicio Local** (${localApiUrl}) esté corriendo en la máquina con la impresora USB. \nDetalle: ${error.response?.data?.detail || error.message}`);
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
.crud-total {
  font-weight: bold;
  margin-top: 10px;
  color: #1e40af;
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
.form-grid {
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
  box-shadow: 8px 8px 16px var(--shadow-light), -8px -8px 16px #ffffff;
  page-break-inside: avoid;
  width: 100%;
  transition: all 0.25s ease-in-out;
}
.etiqueta:hover { transform: translateY(-2px); box-shadow: 12px 12px 24px var(--shadow-light), -12px -12px 24px #ffffff; }
.etiqueta-content { display: flex; justify-content: flex-start; align-items: center; gap: 50px; }
.logo-etiqueta { width: 120px; margin-bottom: 8px; }
.etiqueta-datos { font-size: 1rem; }
.etiqueta-datos .dato { margin-bottom: 12px; }
.etiqueta-qr {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
/* ==== 🎨 NUEVO DISEÑO PROFESIONAL DE ETIQUETAS ==== */
.labels-container {
  justify-content: center;
}

.etiqueta {
  background: #fff;
  border: 2px solid #000;
  border-radius: 6px;
  padding: 14px 18px;
  width: 380px;
  min-height: 230px;
  font-family: 'Courier New', monospace;
  color: #111;
  box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.25s ease-in-out;
}
.etiqueta:hover {
  transform: scale(1.02);
  box-shadow: 5px 5px 16px rgba(0, 0, 0, 0.15);
}
.logo-wrapper {
  text-align: right;
  margin-bottom: 4px;
}
.logo-etiqueta {
  width: 100px;
  object-fit: contain;
}
.etiqueta-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
  border-top: 1px dashed #000;
  padding-top: 8px;
}
.etiqueta-datos .dato {
  font-size: 13px;
  margin-bottom: 4px;
}
.etiqueta-datos strong {
  display: inline-block;
  width: 120px;
}
.barcode {
  position: absolute;
  bottom: 12px;
  left: 18px;
  right: 18px;
  height: 32px;
  background: repeating-linear-gradient(
    to right,
    #000 0px,
    #000 2px,
    #fff 2px,
    #fff 4px
  );
  border-top: 1px solid #000;
  border-bottom: 1px solid #000;
}
@media print {
  @page { size: 100mm 150mm; margin: 4mm; }
  .labels-container {
    gap: 0;
    justify-content: flex-start;
  }
  .etiqueta {
    border: 1px solid #000 !important;
    box-shadow: none !important;
    width: 100%;
    page-break-inside: avoid;
  }
  .barcode {
    background: #000;
    height: 3mm;
  }
}

/* ==== IMPRESIÓN ==== */
@media print {
  @page { size: auto; margin: 0; }
  body { background: none !important; }
  body * { visibility: hidden; background: none !important; box-shadow: none !important; }
  .labels-container, .labels-container * { visibility: visible; background: none !important; box-shadow: none !important; color: black !important; }
  .labels-container { position: absolute; top: 0; left: 0; width: 100%; }
  .etiqueta { display: block; margin: 0; width: 100%; background: none !important; box-shadow: none !important; }  
  .no-print { display: none !important; }
  .logo-fmm {
    width: 70px;
    top: 8px;
    left: 8px;
    opacity: 1;
  }
}

/* ==== PRINTER STATUS ==== */
.printer-status { background: #f3f4f6; color: #111827; font-weight: bold; text-align: center; padding: 8px; border-bottom: 2px solid #e5e7eb; }
.online { color: #22c55e; font-weight: bold; }
.offline { color: #ef4444; font-weight: bold; }

/* ==== MODAL ==== */
.modal-overlay { position: fixed; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 200; }
.modal-card { background: #fff; padding: 20px; border-radius: 16px; width: 400px; max-width: 90%; box-shadow: 8px 8px 20px var(--shadow-light), -8px -8px 20px #ffffff; }
.modal-card h3 { margin-bottom: 16px; color: #1e40af; }
.modal-card .form-field { margin-bottom: 12px; }
.modal-card .form-field label { font-weight: 600; margin-bottom: 4px; display: block; }
.modal-card .form-field input { width: 100%; padding: 8px; border-radius: 8px; border: 1px solid #d1d5db; background: #f9fafb; box-shadow: inset 2px 2px 6px var(--shadow-light), inset -2px -2px 6px #ffffff; }
/* ==== LOGO FMM GLOBAL ==== */
.logo-fmm {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 85px;
  height: auto;
  opacity: 0.95;
  object-fit: contain;
}


/* ==== FORM GRID ==== */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

/* ==== FORM FIELDS ==== */
.form-field {
  background: #f9fafb;
  border-radius: 16px;
  padding: 14px 18px;
  box-shadow: 4px 4px 10px rgba(0,0,0,0.08), -4px -4px 10px #ffffff;
  transition: all 0.25s ease-in-out;
}
.form-field:hover {
  box-shadow: 6px 6px 16px rgba(0,0,0,0.08), -6px -6px 16px #ffffff;
}

/* ==== LABELS ==== */
.crud-label {
  font-weight: 600;
  margin-bottom: 8px;
  display: block;
  color: #1e3a8a;
}

/* ==== INPUTS ==== */
.crud-input, select.crud-input {
  border: none;
  border-radius: 12px;
  width: 100%;
  padding: 10px;
  font-size: 0.95rem;
  background: #f9f9ff;
  box-shadow: inset 2px 2px 6px rgba(0,0,0,0.08), inset -2px -2px 6px #ffffff;
  transition: all 0.25s ease-in-out;
}
.crud-input:focus, select.crud-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.3);
  background: #ffffff;
}

/* ==== PIEZAS POR TARIMA ==== */
.piezas-tarima-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 12px;
  margin-top: 10px;
}

.piezas-tarima-field {
  
  background: #ffeae0;
  border-radius: 14px;
  padding: 8px;
  text-align: center;
  box-shadow: 4px 4px 8px rgba(0,0,0,0.08), -4px -4px 8px #ffffff;
  transition: all 0.25s ease-in-out;
}

.piezas-tarima-field:hover {
  box-shadow: 6px 6px 12px rgba(0,0,0,0.08), -6px -6px 12px #ffffff;
}

.piezas-tarima-input {
  width: 40%;
  text-align: center;
  border: none;
  border-radius: 10px;
  text-align: center;
  font-weight: 60;
  font-size: 0.95rem;
  padding: 18px 0;
  background: #f9f9ff;
  box-shadow: inset 2px 2px 6px rgba(0,0,0,0.08), inset -2px -2px 6px #ffffff;
  transition: all 0.25s ease-in-out;
}

.piezas-tarima-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.3);
  background: #ffffff;
}

/* ==== TARIMAS CARD ==== */
.crud-card {
  background: white;
  border-radius: 20px;
  padding: 26px;
  box-shadow: 12px 12px 24px rgba(0,0,0,0.08), -12px -12px 24px #ffffff;
  transition: all 0.3s ease-in-out;
}
.crud-card:hover {
  transform: translateY(-3px);
  box-shadow: 16px 16px 32px rgba(0,0,0,0.08), -16px -16px 32px #ffffff;
}

/* ==== SUBTITLES ==== */
.crud-subtitle {
  font-size: 28px;
  font-weight: 700;
  color: #1f618d;
  margin-bottom: 20px;
  border-left: 6px solid #2980b9;
  padding-left: 12px;
}



/* ==== BOTONES CENTRADOS ==== */
.crud-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}
.btn {
  padding: 12px 22px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  transition: all 0.25s ease-in-out;
  box-shadow: 6px 6px 12px rgba(0,0,0,0.08), -6px -6px 12px #ffffff;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 8px 8px 16px rgba(0,0,0,0.08), -8px -8px 16px #ffffff;
}
.btn-print { background: linear-gradient(135deg, #22c55e, #16a34a); color: white; }
.btn-reset { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: white; }
.btn-save { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; }

/* ==== INPUT DESHABILITADO ==== */
.bg-gray-100 {
  background: #f3f4f6;
  box-shadow: inset 2px 2px 6px rgba(0,0,0,0.08), inset -2px -2px 6px #ffffff;
  border-radius: 12px;
}



.labels-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 20px;
}

.etiqueta-preview {
  width: 220px;
  min-height: 140px;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 4px 4px 10px rgba(0,0,0,0.05);
  background: #fff;
  position: relative;
}

.etiqueta-preview .logo-fmm {
  width: 40px;
  position: absolute;
  top: 8px;
  left: 8px;
}

.etiqueta-preview .logo-etiqueta {
  width: 50px;
  margin-bottom: 6px;
}

.etiqueta-preview .etiqueta-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.etiqueta-preview .etiqueta-datos {
  font-size: 0.8rem;
}

.etiqueta-preview .etiqueta-qr {
  margin-left: 8px;
}

</style>


