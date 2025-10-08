<template>
  <div class="login-wrapper">
    <div class="login-card" :class="{ 'enter-card': animateCard }">
      
      <!-- Imagen con rebote -->
      <img src="@/assets/login.svg" alt="Login Imagen" class="login-img"/>

      <!-- Título -->
      <h1 class="login-title">
        <span class="highlight">BIENVENIDO<span class="green-dot">.</span></span>
      </h1>

      <!-- Formulario con animación secuencial -->
      <transition-group name="fade-slide" tag="div">

        <!-- Sede -->
        <div v-if="animateCard" class="input-group" key="sede">
          <label>Sede</label>
          <select v-model="sede" class="login-select">
            <option disabled value="">Selecciona tu sede</option>
            <option value="Guadalajara">Guadalajara</option>
            <option value="Mexico">México</option>
          </select>
        </div>

        <!-- Rol -->
        <div v-if="sede" class="input-group" key="rol">
          <label>Rol</label>
          <select v-model="rol" class="login-select">
            <option disabled value="">Selecciona tu rol</option>
            <option value="Practicante">Practicante</option>
            <option value="Coordinador">Coordinador</option>
          </select>
        </div>

        <!-- Usuario -->
        <div class="input-group" key="usuario">
          <label>Usuario</label>
          <input v-model="username" type="text" placeholder="Ingresa tu nombre" class="login-input"/>
        </div>

        <!-- Contraseña -->
        <div v-if="rol" class="input-group" key="password">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="Ingresa tu contraseña" class="login-input"/>
        </div>

        <!-- Botones -->
        <button @click="login" class="login-btn" key="btn">Ingresar</button>
        <button v-if="rol === 'Coordinador'" @click="registrarCoordinador" class="registrar-btn" key="register">Registrar</button>

      </transition-group>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserLogin",
  data() {
    return {
      username: "",
      password: "",
      sede: "",
      rol: "",
      animateCard: false
    };
  },
  mounted() {
    // Animación inicial
    setTimeout(() => {
      this.animateCard = true;
    }, 100);
  },
  methods: {
    async login() {
      if (!this.username || !this.password || !this.rol || !this.sede) {
        alert("Debes ingresar usuario, contraseña, sede y rol");
        return;
      }

      try {
        const formData = new FormData();
        formData.append("nombre", this.username);
        formData.append("contrasena", this.password);

        let url = "";

        // Login para cada tipo de usuario
        if (this.rol === "Practicante") {
          url = "http://127.0.0.1:8000/user_practicantes/login";
        } else if (this.rol === "Coordinador") {
          url = "http://127.0.0.1:8000/user_coordinadors/login";
        }

        const res = await axios.post(url, formData);

        // Guardar datos en localStorage
        localStorage.setItem("username", res.data.nombre);
        localStorage.setItem("rol", this.rol);
        localStorage.setItem("token", res.data.token);
        localStorage.setItem("sede", this.sede);
        localStorage.setItem("user_id", res.data.user_id);

        // Redirigir según rol y sede
        const destino =
          this.rol === "Practicante"
            ? `/${this.sede.toLowerCase()}/practicante`
            : `/${this.sede.toLowerCase()}/coordinador`;

        this.$router.push(destino);

      } catch (err) {
        console.error("❌ Error en login:", err);
        alert(err.response?.data?.detail || "Error al iniciar sesión");
      }
    },

    registrarCoordinador() {
      this.$router.push("/registro");
    }
  }
};
</script>

<style scoped>
/* Fondo principal */
.login-wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #0F1973;
  font-family: "Poppins", sans-serif;
}

/* Tarjeta */
.login-card {
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
.login-card.enter-card {
  transform: translateY(0);
  opacity: 1;
}

/* Imagen con rebote */
.login-img {
  width: 330px;
  height: 100px;
  object-fit: contain;
  margin-bottom: 0px;
  margin-top: auto;
  animation: bounce 1.5s infinite alternate;
}
@keyframes bounce { 0% { transform: translateY(0);} 100% { transform: translateY(-10px);} }

/* Título */
.highlight {
  font-size: 3rem;
  font-weight: 900;
  color: #F4550F;
  text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
}
.green-dot {
  color: #64C22C;
  text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
}

/* Inputs */
.input-group { margin-bottom: 20px; text-align: left; }
.input-group label { display: block; font-weight: 600; margin-bottom: 5px; color: #0F1973; }
.login-input, .login-select {
  width: 100%;
  padding: 12px 15px;
  border-radius: 10px;
  border: 1px solid #ddd;
  font-size: 1rem;
  transition: border 0.3s, box-shadow 0.3s;
}
.login-input:focus, .login-select:focus {
  border-color: #F4550F;
  box-shadow: 0 0 10px rgba(244,85,15,0.5);
  outline: none;
}

/* Botones */
.login-btn, .registrar-btn {
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
.login-btn {
  background: linear-gradient(135deg, #F4550F, #F4772E);
  color: white;
}
.login-btn:hover {
  background: linear-gradient(135deg, #F4772E, #F4550F);
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 20px rgba(244,85,15,0.4);
}
.registrar-btn {
  background: #e5e7eb;
  color: #111827;
}
.registrar-btn:hover {
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
</style>
