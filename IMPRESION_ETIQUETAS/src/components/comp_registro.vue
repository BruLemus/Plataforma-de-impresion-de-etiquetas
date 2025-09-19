<template>
  <div class="register-wrapper">
    <div class="register-background">
      <div class="register-card">
        <h1 class="register-title">Registro de Coordinador</h1>

        <div class="register-image">
          <img src="@/assets/e1.png" alt="Registro Imagen" />
        </div>

        <!-- Nombre -->
        <input
          v-model="nombre"
          type="text"
          placeholder="Ingresa tu nombre"
          class="register-input"
        />

        <!-- contrasena -->
        <input
          v-model="contrasena"
          type="password"
          placeholder="Ingresa tu contrasena"
          class="register-input"
        />

        <!-- Código secreto -->
        <input
          v-model="codigoSecreto"
          type="password"
          placeholder="Ingresa el código secreto"
          class="register-input"
        />

        <button @click="registrar" class="register-btn">Registrar</button>
        <button @click="volverLogin" class="volver-btn">Volver al login</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserCoordinadorRegister",
  data() {
    return {
      nombre: "",
      contrasena: "",
      codigoSecreto: ""
    };
  },
  methods: {
    async registrar() {
      if (!this.nombre || !this.contrasena || !this.codigoSecreto) {
        alert("Todos los campos son obligatorios");
        return;
      }

      try {
        const payload = {
          nombre: this.nombre,
          contrasena: this.contrasena,
          codigo_secreto: this.codigoSecreto
        };

        const res = await axios.post(
          "http://127.0.0.1:8000/user_coordinadors/",
          payload
        );

        alert(`Coordinador ${res.data.nombre} registrado correctamente`);
        this.$router.push("/");
      } catch (error) {
        alert(error.response?.data?.detail || "Error al registrar coordinador");
      }
    },
    volverLogin() {
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
/* Fondo y centrado */
.register-wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to right, #bfc4d6, #9cacc4);
  padding: 20px;
}

/* Tarjeta */
.register-card {
  background: white;
  border-radius: 16px;
  padding: 60px 40px;
  max-width: 700px;
  width: 90%;
  text-align: center;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
  position: relative;
  transition: all 0.3s ease;
}

/* Título */
.register-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 25px;
  color: #1e3a8a;
  line-height: 1.2;
}

/* Imagen */
.register-image {
  height: 250px;
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 12px;
}

/* Input */
.register-input {
  width: 90%;
  padding: 14px;
  margin-bottom: 20px;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 1.2rem;
}

/* Botones */
.register-btn {
  width: 60%;
  padding: 14px;
  border-radius: 10px;
  border: none;
  background: #0fa8cb;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.3s;
  margin-bottom: 10px;
}

.volver-btn {
  width: 50%;
  padding: 14px;
  border-radius: 10px;
  border: none;
  background: #afb7ac;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.3s;
}

.register-btn:hover {
  background: #a9b8e2;
}

/* ===== Media Queries ===== */
@media (max-width: 768px) {
  .register-card {
    padding: 40px 25px;
    width: 95%;
  }
  .register-title {
    font-size: 2rem;
  }
  .register-image {
    height: 180px;
  }
  .register-input {
    font-size: 1rem;
  }
  .register-btn, .volver-btn {
    font-size: 1rem;
    width: 70%;
  }
}

@media (max-width: 480px) {
  .register-card {
    padding: 30px 20px;
  }
  .register-title {
    font-size: 1.7rem;
  }
  .register-image {
    height: 150px;
  }
  .register-input {
    font-size: 0.95rem;
  }
  .register-btn, .volver-btn {
    font-size: 0.95rem;
    width: 80%;
  }
}
</style>
