<template>
 <div class="crud-card">
 <h2 class="crud-subtitle">⚠️ Impresión de Otras Etiquetas</h2>

<div class="form-grid">
<div class="form-field">
<label class="crud-label">Tipo de Etiqueta</label>
<select v-model="tipoEtiqueta" class="crud-input" :disabled="isPrinting">
<option value="fragil">Frágil</option>
 <option value="hacia_arriba">Hacia Arriba</option>
</select>
 </div>

<div class="form-field">
<label class="crud-label">Cantidad</label>
<input type="number" v-model="cantidad" min="1" class="crud-input" :disabled="isPrinting" />
</div>
</div>

<div class="preview-container">
<h3 class="preview-title">Vista Previa</h3>
<div v-if="tipoEtiqueta === 'fragil'" class="preview-box">
<img src="@/assets/fragil.png" alt="Etiqueta Frágil" />
</div>
<div v-else-if="tipoEtiqueta === 'hacia_arriba'" class="preview-box">
<img src="@/assets/arriba.png" alt="Etiqueta Hacia Arriba" />
</div>
</div>

<div class="form-actions">
<button @click="imprimirEtiquetas" class="crud-button" :disabled="isPrinting">
<span v-if="isPrinting">🖨️ Enviando...</span>
<span v-else>🖨️ Imprimir</span>
</button>
</div>
</div>
</template>

<script>
// Ajusta esta URL base a la dirección de tu servidor FastAPI
const API_BASE_URL = "http://localhost:8000"; 

export default {
   name: "comp_otras_etiquetas",
   data() {
      return {
         tipoEtiqueta: "fragil",
         cantidad: 1,
      isPrinting: false, // Controlar el estado de carga
      };
   },
   methods: {
      async imprimirEtiquetas() {
         if (this.isPrinting) return; 
         
         if (!this.cantidad || this.cantidad < 1) {
 alert("Ingresa una cantidad válida (mínimo 1)");
 return;
         }

         this.isPrinting = true;
      let printSuccess = false;

         try {
 // 1. Prepara los datos para el endpoint de FastAPI
 const payload = {
    tipo_etiqueta: this.tipoEtiqueta,
    cantidad: parseInt(this.cantidad, 10),
 };

 console.log("Enviando solicitud de impresión al backend:", payload);

 // 2. Llama al endpoint de FastAPI. El backend se encargará de GENERAR y ENVIAR el ZPL.
 const response = await fetch(`${API_BASE_URL}/imprimir/generate_other_label`, {
    method: 'POST',
    headers: {
       'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
 });

 const data = await response.json();

 if (!response.ok || data.error) {
    throw new Error(`El servidor reportó un error: ${data.error || response.statusText}`);
 }
        
        printSuccess = true;

         } catch (error) {
 console.error('Error en el proceso de impresión:', error);
 alert(`❌ Error al intentar imprimir. Mensaje: ${error.message}`);
         } finally {
 this.isPrinting = false;
        if (printSuccess) {
            alert(`✅ Éxito! Se enviaron ${this.cantidad} etiquetas de "${this.tipoEtiqueta}" a la impresora.`);
        }
         }
      },
   },
};
</script>

<style scoped>
/* (Estilos CSS sin cambios) */
.crud-card { max-width: 400px; margin: 20px auto; padding: 18px; border-radius: 14px; background: #ffffff; box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.08); transition: all 0.3s ease-in-out; }
.crud-card:hover { transform: scale(1.01); }
.crud-subtitle { font-size: 18px; font-weight: bold; margin-bottom: 18px; text-align: center; padding: 10px; border-radius: 10px; background: linear-gradient(135deg, #a2b6f3); color: rgb(0, 0, 0); box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2); }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-bottom: 20px; }
.form-field { display: flex; flex-direction: column; }
.crud-label { font-weight: 600; margin-bottom: 6px; color: #333; }
.crud-input { padding: 8px; border: 1px solid #ccc; border-radius: 8px; transition: 0.3s; }
.crud-input:focus { outline: none; border-color: #3b82f6; box-shadow: 0px 0px 6px rgba(59, 130, 246, 0.4); }
.preview-container { margin: 20px 0; text-align: center; }
.preview-title { font-size: 15px; margin-bottom: 10px; color: #555; font-weight: 600; }
.preview-box { display: inline-block; padding: 12px; border: 2px dashed #3b82f6; border-radius: 10px; background: #f9fafb; }
.preview-box img { max-width: 150px; max-height: 150px; object-fit: contain; }
.form-actions { text-align: center; margin-top: 10px; }
.crud-button { background: #197d3e; color: white; padding: 10px 18px; border: none; border-radius: 8px; cursor: pointer; font-size: 15px; font-weight: bold; transition: 0.3s; }
.crud-button:hover { background: #43a166; }
.crud-button:disabled { background: #90a4ae; cursor: not-allowed; }
</style>