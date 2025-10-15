<template>
  <div class="crud-card no-print">
    <h2 class="crud-subtitle">Etiquetas por Tarima</h2>

    <div class="form-grid">
      <!-- Paquetería -->
      <div class="form-field">
        <label class="crud-label">Paquetería</label>
        <select v-model="paqueteriaSeleccionada" class="crud-input">
          <option disabled value="">-- Selecciona --</option>
          <option v-for="paq in paqueterias" :key="paq" :value="paq">{{ paq }}</option>
        </select>
      </div>

      <!-- Factura -->
      <div class="form-field">
        <label class="crud-label">Número de Factura</label>
        <input v-model="factura" type="text" class="crud-input" placeholder="Factura" />
      </div>

      <!-- Número de Tarimas -->
      <div class="form-field">
        <label class="crud-label">Número de Tarimas</label>
        <input v-model.number="numTarimas" type="number" min="1" class="crud-input" placeholder="Ej: 2" />
      </div>

      <!-- Tipo de Embalaje -->
      <div class="form-field">
        <label class="crud-label">Tipo de Embalaje</label>
        <select v-model.number="tipoEmbalaje" class="crud-input">
          <option disabled value="">-- Selecciona --</option>
          <option v-for="n in 3" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <!-- Clave de Producto -->
      <div class="form-field">
        <label class="crud-label">Clave de Producto</label>
        <input v-model="claveProducto" type="text" class="crud-input" placeholder="Clave del producto" />
      </div>

      <!-- Campos solo para Estafeta y Paquetexpress -->
      <template v-if="requiereDimensiones">
        <div class="form-field">
          <label class="crud-label">Ancho (cm)</label>
          <input v-model.number="ancho" type="number" min="0" class="crud-input" placeholder="Ej: 120" />
        </div>
        <div class="form-field">
          <label class="crud-label">Largo (cm)</label>
          <input v-model.number="largo" type="number" min="0" class="crud-input" placeholder="Ej: 80" />
        </div>
        <div class="form-field">
          <label class="crud-label">Alto (cm)</label>
          <input v-model.number="alto" type="number" min="0" class="crud-input" placeholder="Ej: 150" />
        </div>
        <div class="form-field">
          <label class="crud-label">Peso (kg)</label>
          <input v-model.number="peso" type="number" min="0" step="0.01" class="crud-input" placeholder="Ej: 12.5" />
        </div>
        <div class="form-field">
          <label class="crud-label">Peso Volumétrico (kg)</label>
          <input :value="pesoVolumetrico.toFixed(2)" type="number" disabled class="crud-input bg-gray-100" />
        </div>
      </template>
    </div>

    <!-- PIEZAS POR TARIMA -->
    <div v-if="numTarimas > 0" class="form-grid">
      <div v-for="(pieza, index) in piezas" :key="'pieza-' + index" class="form-field">
        <label class="crud-label">Piezas Tarima {{ index + 1 }}</label>
        <input v-model.number="piezas[index]" type="number" min="0" class="crud-input" />
      </div>
    </div>

    <div class="crud-total">Total de piezas: {{ totalPiezas }}</div>

    <!-- BOTONES -->
    <div class="crud-actions no-print">
      <button @click="imprimir" class="btn btn-print">🖨️ Imprimir</button>
      <button @click="reiniciar" class="btn btn-reset">🔄 Reiniciar</button>
      <button @click="guardarDatos" class="btn btn-save">💾 Guardar</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      paqueterias: ["Paquetexpress", "Estafeta", "DHL", "FedEx", "UPS", "MercadoLibre"],
      paqueteriaSeleccionada: "",
      factura: "",
      numTarimas: 0,
      tipoEmbalaje: null,
      claveProducto: "",
      ancho: 0,
      largo: 0,
      alto: 0,
      peso: 0,
      piezas: [],
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
    requiereDimensiones() {
      return (
        this.paqueteriaSeleccionada === "Estafeta" ||
        this.paqueteriaSeleccionada === "Paquetexpress"
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
      this.paqueteriaSeleccionada = "";
      this.tipoEmbalaje = null;
      this.claveProducto = "";
      this.ancho = 0;
      this.largo = 0;
      this.alto = 0;
      this.peso = 0;
      this.piezas = [];
    },

async guardarDatos() {
  if (
    !this.factura ||
    !this.tipoEmbalaje ||
    !this.paqueteriaSeleccionada ||
    !this.claveProducto
  ) {
    return alert("Completa todos los campos obligatorios");
  }

  try {
    const token = localStorage.getItem("token");
    const id = localStorage.getItem("id");
    const username = localStorage.getItem("username");
    const sede = localStorage.getItem("sede")
    let role = localStorage.getItem("rol"); // "coordinador" o "practicante"
    role = role?.toLowerCase() || "practicante"; // asegurar minúsculas


    // 🔹 Construcción del payload
    const payload = {
      numero_facturas: this.factura,
      numero_tarimas: Number(this.numTarimas) || 0,
      tipo_embalaje: Number(this.tipoEmbalaje),
      paqueteria: this.paqueteriaSeleccionada,
      clave_producto: this.claveProducto,
      cantidad_piezas: this.totalPiezas,
      ancho: this.requiereDimensiones ? Number(this.ancho) : 0,
      largo: this.requiereDimensiones ? Number(this.largo) : 0,
      alto: this.requiereDimensiones ? Number(this.alto) : 0,
      peso: this.requiereDimensiones ? Number(this.peso) : 0,
      peso_volumetrico: this.requiereDimensiones
        ? Number(this.pesoVolumetrico.toFixed(2))
        : 0,

      practicante_id: role === "practicante" ? Number(id) : null,
      coordinador_id: role === "coordinador" ? Number(id) : null,

      nombre_user_practicante:
        role === "practicante" ? username || "" : "",
      nombre_user_coordinador:
        role === "coordinador" ? username || "" : "",
    };

    console.log("📦 Enviando payload:", payload);

    // 🔹 URL con sede y role
    const response = await fetch(
      `http://127.0.0.1:8000/tarimas/?sede=${sede}&role=${role}`,
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
      return alert(
        "Error al guardar en la base de datos: " +
          (data.detail ? JSON.stringify(data.detail) : data)
      );
    }

    alert("✅ Datos guardados correctamente");
    this.reiniciar();
  } catch (err) {
    console.error(err);
    alert("❌ Ocurrió un error al guardar los datos");
  }
},




    async imprimir() {
      if (!this.numTarimas || this.numTarimas <= 0)
        return alert("No hay etiquetas para imprimir");

      const contenido = `
Paquetería: ${this.paqueteriaSeleccionada}
Factura: ${this.factura}
Número de Tarimas: ${this.numTarimas}
Tipo de Embalaje: ${this.tipoEmbalaje}
Clave Producto: ${this.claveProducto}
${this.requiereDimensiones ? `Ancho: ${this.ancho} cm\nLargo: ${this.largo} cm\nAlto: ${this.alto} cm\nPeso: ${this.peso} kg\nPeso Volumétrico: ${this.pesoVolumetrico.toFixed(2)} kg\n` : ""}
Total piezas: ${this.totalPiezas}
`;

      try {
        const res = await fetch("http://127.0.0.1:8000/imprimir/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ contenido }),
        });

        const data = await res.json();
        if (data.status === "ok") alert("Se envió a imprimir correctamente");
        else alert("Error al imprimir: " + data.message);
      } catch (err) {
        console.error(err);
        alert("Ocurrió un error al enviar la impresión");
      }
    },
  },
};
</script>
<style scoped>
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

/* ==== TOTAL PIEZAS ==== */
.crud-total {
  font-weight: bold;
  margin-top: 10px;
  color: #1e40af;
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
</style>



