<template>
  <div class="register-wrapper">
    <div class="register-card" :class="{ 'enter-card': animateCard }">
      
      <!-- Imagen con rebote -->
      <img src="@/assets/login.svg" alt="Registro Imagen" class="register-img"/>

      <!-- Título -->
      <h1 class="register-title">
        <span class="highlight">Registro de Coordinador</span>
      </h1>

      <!-- Inputs animados -->
      <transition-group name="fade-slide" tag="div">

        <!-- Nombre -->
        <div class="input-group" key="nombre">
          <label>Nombre</label>
          <input v-model="nombre" type="text" placeholder="Ingresa tu nombre" class="register-input"/>
        </div>

        <!-- Contraseña -->
        <div class="input-group" key="contrasena">
          <label>Contraseña</label>
          <input v-model="contrasena" type="password" placeholder="Ingresa tu contraseña" class="register-input"/>
        </div>

        <!-- Código secreto -->
        <div class="input-group" key="codigo">
          <label>Código secreto</label>
          <input v-model="codigoSecreto" type="password" placeholder="Ingresa el código secreto" class="register-input"/>
        </div>

        <!-- Botones -->
        <button @click="registrar" class="register-btn" key="btn">Registrar</button>
        <button @click="volverLogin" class="volver-btn" key="volver">Volver al login</button>

      </transition-group>

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
      codigoSecreto: "",
      animateCard: false
    };
  },
  mounted() {
    setTimeout(() => { this.animateCard = true; }, 100);
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
        const res = await axios.post("http://127.0.0.1:8000/user_coordinadors/", payload);
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
/* Fondo principal */
.register-wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #0F1973; /* azul */
  font-family: "Poppins", sans-serif;
}


/* Tarjeta */
.register-card {
  background: #FFFFFF;
  border-radius: 25px;
  padding: 50px 40px;
  max-width: 500px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  transform: translateY(-40px);
  opacity: 0;
  transition: all 0.8s ease;
}
.register-card.enter-card {
  transform: translateY(0);
  opacity: 1;
}

/* Imagen con rebote */
.register-img {
  object-fit: contain;
  animation: bounce 1.5s infinite alternate;
  width: 330px;
  height: 100px;
  object-fit: contain;
  margin-bottom: 0px;
  margin-top: auto;

}
@keyframes bounce { 0% { transform: translateY(0);} 100% { transform: translateY(-10px);} }

/* Título */
.register-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #F4550F; /* naranja */
  text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
  margin-bottom: 25px;
}
.highlight { color: #F4550F; }
.green-dot { color: #64C22C; }

/* Inputs */
.input-group { margin-bottom: 20px; text-align: left; }
.input-group label { display: block; font-weight: 600; margin-bottom: 5px; color: #0F1973; }
.register-input {
  width: 100%;
  padding: 12px 15px;
  border-radius: 10px;
  border: 1px solid #ddd;
  font-size: 1rem;
  transition: border 0.3s, box-shadow 0.3s;
}
.register-input:focus {
  border-color: #F4550F;
  box-shadow: 0 0 10px rgba(244,85,15,0.5);
  outline: none;
}

/* Botones */
.register-btn, .volver-btn {
  width: 100%;
  padding: 14px;
  margin-top: 10px;
  border-radius: 12px;
  border: none;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}
.register-btn {
  background: linear-gradient(135deg, #F4550F, #F4772E);
  color: white;
}
.register-btn:hover {
  background: linear-gradient(135deg, #F4772E, #F4550F);
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 20px rgba(244,85,15,0.4);
}
.volver-btn {
  background: #e5e7eb;
  color: #111827;
}
.volver-btn:hover {
  background: #d1d5db;
  transform: translateY(-2px) scale(1.02);
}

/* Animación inputs secuenciales */
.fade-slide-enter-active {
  transition: all 0.5s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

/* Responsive */
@media (max-width: 480px) {
  .register-card { padding: 40px 20px; }
  .register-title { font-size: 2rem; }
  .register-img { width: 150px; height: 150px; }
  .register-input, .register-btn, .volver-btn { font-size: 0.95rem; }
}
</style>
