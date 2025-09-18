<template>
  <div class="crud-card">
    <!-- Título -->
    <h2 class="crud-subtitle">Registro de Roles</h2>

    <!-- Formulario -->
    <form @submit.prevent="guardarDatos">
      <!-- Select de Rol -->
      <div class="form-group">
        <label for="rol">Rol</label>
        <select v-model="form.rol" id="rol" required>
          <option disabled value="">Seleccione un rol</option>
          <option v-for="opcion in rolesDisponibles" :key="opcion" :value="opcion">
            {{ opcion }}
          </option>
        </select>
      </div>

      <!-- Usuario -->
      <div class="form-group">
        <label for="usuario">Usuario</label>
        <input
          v-model="form.usuario"
          type="text"
          nombre="usuario"
          required
          placeholder="Ingrese el usuario"
        />
      </div>

      <!-- Botón Guardar -->
      <button type="submit" class="btn-guardar">Guardar</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegistroRol",
  data() {
    return {
      form: {
        UserRol: "",
        usuario: "",
      },
      rolesDisponibles: [
        "Practicante",
        "Coordinador",
       
      ],
    };
  },
  methods: {
    async guardarDatos() {
      try {
        // Obtener número de mesa desde el login
        const numeroMesa = localStorage.getItem("numeroMesa");

        const payload = {
          rol: this.form.rol,
          usuario: this.form.usuario,
          mesa: numeroMesa, 
        };

        await axios.post("http://127.0.0.1:8000/rols/", payload);

        alert("Registro guardado correctamente ✅");

        // Limpiar formulario
        this.form.rol = "";
        this.form.usuario = "";
      } catch (error) {
        console.error("Error al guardar:", error);
        alert("❌ Error al guardar el registro");
      }
    },
  },
};
</script>

<style scoped>
.crud-card {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  background: #fff;
}

.crud-subtitle {
  text-align: center;
  margin-bottom: 20px;
  font-size: 22px;
  font-weight: bold;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #444;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.btn-guardar {
  width: 100%;
  padding: 10px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  font-weight: bold;
}

.btn-guardar:hover {
  background: #43a047;
}
</style>
