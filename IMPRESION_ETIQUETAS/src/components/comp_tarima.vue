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

      <!-- Dimensiones solo si es Estafeta -->
      <div v-if="paqueteriaSeleccionada === 'Estafeta'" class="form-field">
        <label class="crud-label">Ancho (cm)</label>
        <input v-model.number="ancho" type="number" min="0" class="crud-input" placeholder="Ej: 120" />
      </div>
      <div v-if="paqueteriaSeleccionada === 'Estafeta'" class="form-field">
        <label class="crud-label">Largo (cm)</label>
        <input v-model.number="largo" type="number" min="0" class="crud-input" placeholder="Ej: 80" />
      </div>
      <div v-if="paqueteriaSeleccionada === 'Estafeta'" class="form-field">
        <label class="crud-label">Alto (cm)</label>
        <input v-model.number="alto" type="number" min="0" class="crud-input" placeholder="Ej: 150" />
      </div>
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
  },
  methods: {
    // --- AJUSTE: Imprimir directamente a la impresora de red ---
    async imprimir() {
      if (!this.numTarimas || this.numTarimas <= 0)
        return alert("No hay etiquetas para imprimir");

      // Construir contenido a imprimir (puedes personalizar formato)
      const contenido = `
Paquetería: ${this.paqueteriaSeleccionada}
Factura: ${this.factura}
Número de Tarimas: ${this.numTarimas}
Tipo de Embalaje: ${this.tipoEmbalaje}
Clave Producto: ${this.claveProducto}
Total piezas: ${this.totalPiezas}
`;

      try {
        const res = await fetch("http://127.0.0.1:8000/imprimir/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ contenido })
        });

        const data = await res.json();
        if (data.status === "ok") alert("Se envió a imprimir correctamente");
        else alert("Error al imprimir: " + data.message);

      } catch (err) {
        console.error(err);
        alert("Ocurrió un error al enviar la impresión");
      }
    },

    reiniciar() {
      this.factura = "";
      this.numTarimas = 0;
      this.paqueteriaSeleccionada = "";
      this.tipoEmbalaje = null;
      this.claveProducto = "";
      this.ancho = 0;
      this.largo = 0;
      this.alto = 0;
      this.piezas = [];
    },

    async guardarDatos() {
      if (!this.factura || !this.paqueteriaSeleccionada || !this.tipoEmbalaje || !this.numTarimas) {
        return alert("Factura, Paquetería, Tipo de Embalaje y Número de Tarimas son obligatorios");
      }

      try {
        const payload = {
          paqueteria: this.paqueteriaSeleccionada,
          numero_factura: this.factura,
          numero_tarimas: Number(this.numTarimas),
          tipo_embalaje: Number(this.tipoEmbalaje),
          ancho: this.paqueteriaSeleccionada === "Estafeta" ? Number(this.ancho) : 0,
          largo: this.paqueteriaSeleccionada === "Estafeta" ? Number(this.largo) : 0,
          alto: this.paqueteriaSeleccionada === "Estafeta" ? Number(this.alto) : 0,
          cantidad_piezas: Number(this.totalPiezas),
          clave_producto: this.claveProducto || "N/A"
        };

        console.log("Payload a enviar:", payload);

        const response = await fetch("http://127.0.0.1:8000/tarimas/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Error API:", errorData);
          throw new Error("Error al guardar en la base de datos");
        }

        alert("Datos guardados correctamente");
        this.reiniciar();
      } catch (err) {
        console.error(err);
        alert("Ocurrió un error al guardar los datos");
      }
    },
  },
};
</script>

<style scoped>
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 20px; }
.form-field { background: #f9fafb; border-radius: 12px; padding: 14px 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.crud-label { font-weight: 600; margin-bottom: 8px; display: block; color: #1e3a8a; }
.crud-input { border: 1px solid #d1d5db; border-radius: 8px; width: 100%; padding: 10px; font-size: 0.95rem; }
.crud-card { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
.crud-subtitle { font-weight: 600; margin-bottom: 12px; color: #1e40af; font-size: 1.05rem; }
.pieces-grid { display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 10px; }
.piece-card { background: #e0f2fe; border-radius: 10px; padding: 10px 14px; display: flex; flex-direction: column; align-items: center; min-width: 90px; transition: all 0.2s; }
.crud-label-inline { font-weight: 600; margin-bottom: 6px; text-align: center; }
.crud-input-small { border: 1px solid #9ca3af; border-radius: 6px; width: 60px; padding: 6px; font-size: 0.9rem; text-align: center; }
.crud-actions { display: flex; gap: 12px; margin-top: 16px; }
.btn { padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
.btn-print { background: #126330; color: white; }
.btn-reset { background: #cd981c; color: white; }
.btn-save { background: #2559ac; color: white; }
.crud-total { font-weight: bold; margin-top: 10px; color: #1e40af; }
</style>
