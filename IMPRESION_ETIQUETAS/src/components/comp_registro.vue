<template>
  <div class="crud-card">
    <h2 class="crud-subtitle">Registro de Coordinador</h2>

    <form @submit.prevent="guardarDatos">
      <!-- Nombre -->
      <div class="form-group">
        <label for="nombre">Nombre</label>
        <input
          v-model="form.nombre"
          type="text"
          id="nombre"
          required
          placeholder="Ingrese el nombre"
        />
      </div>

      <!-- Contraseña -->
      <div class="form-group">
        <label for="contrasena">Contraseña</label>
        <input
          v-model="form.contrasena"
          type="password"
          id="contrasena"
          required
          placeholder="Ingrese la contraseña"
        />
      </div>

      <button type="submit" class="btn-guardar">Guardar</button>

      <router-link to="/" class="btn-cancelar">Ya tengo una cuenta</router-link>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegistroCoordinador",
  data() {
    return {
      form: {
        nombre: "",
        contrasena: "",
      },
    };
  },
  methods: {
    async guardarDatos() {
      try {
        const payload = {
          nombre: this.form.nombre,
          UserRol: "Coordinador",
          contrasena: this.form.contrasena,
          mesa_trabajo: this.mesaTrabajo || "",
          salida: this.salida || null
        };

        console.log("Payload a enviar:", payload);

        await axios.post("http://127.0.0.1:8000/user_rols/", payload);

        alert("Coordinador registrado correctamente ✅");

        // Limpiar formulario
        this.form.nombre = "";
        this.form.contrasena = "";
      } catch (error) {
        console.error("Error al guardar:", error.response?.data || error);
        alert("❌ Error al registrar el coordinador");
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
.btn-cancelar {
  display: inline-block;
  margin-top: 10px;
  text-align: center;
  width: 50%;
  padding: 10px;
  background: #7d997e;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  font-weight: bold;
  text-decoration: none;
  
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.btn-guardar {
  width: 100%;
  padding: 10px;
  background: #0fa8cb;
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
