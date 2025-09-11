<!-- src/components/UserLogin.vue -->
<template>
  <div class="login-wrapper">
    <div class="login-background">
      <div class="login-card">

        <!-- Título -->
        <h1 class="login-title">Bienvenido</h1>

        <!-- Imagen fija -->
        <div class="login-image">
          <img src="@/assets/img_login.png" alt="Login Imagen" />
        </div>

        <!-- Formulario -->
        <input
          v-model="username"
          type="text"
          placeholder="Ingresa tu nombre"
          class="login-input"
        />

        <!-- Selección de Mesa -->
        <select v-model="mesa" class="login-select">
          <option disabled value="">Selecciona la mesa</option>
          <option v-for="n in 10" :key="n" :value="n">
            Mesa {{ n }}
          </option>
        </select>

        <button @click="login" class="login-btn">Ingresar</button>
      </div>      
    </div>
  </div>
</template>

<script>
export default {
  name: "UserLogin",
  data() {
    return {
      username: "",
      mesa: ""
    };
  },
  methods: {
    login() {
      if (!this.username.trim()) return alert("Ingresa tu nombre");
      if (!this.mesa) return alert("Selecciona una mesa");

      localStorage.setItem("username", this.username);
      localStorage.setItem("mesa", this.mesa);

      this.$router.push("/etiquetas");
    },
  },
};
</script>

<style scoped>
/* Fondo y centrado */
.login-wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to right, #bfc4d6, #9cacc4);
  padding: 20px;
}

/* Tarjeta */
.login-card {
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
.login-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 25px;
  color: #1e3a8a;
  line-height: 1.2;
}

/* Imagen */
.login-image {
  height: 250px;
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 12px;
}

/* Input y select */
.login-input,
.login-select {
  width: 90%;
  padding: 14px;
  margin-bottom: 20px;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 1.2rem;
}

.login-select {
  background: #f9fafb;
  cursor: pointer;
}

/* Botón */
.login-btn {
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
}

.login-btn:hover {
  background: #a9b8e2;
}

/* ===== Media Queries ===== */
@media (max-width: 1024px) {
  .login-card {
    padding: 50px 30px;
  }
  .login-title {
    font-size: 2.5rem;
  }
  .login-image {
    height: 200px;
  }
}

@media (max-width: 768px) {
  .login-card {
    padding: 40px 25px;
    width: 95%;
  }
  .login-title {
    font-size: 2rem;
  }
  .login-image {
    height: 180px;
  }
  .login-input,
  .login-select {
    font-size: 1rem;
  }
  .login-btn {
    font-size: 1rem;
    width: 70%;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
  .login-title {
    font-size: 1.7rem;
  }
  .login-image {
    height: 150px;
  }
  .login-input,
  .login-select {
    font-size: 0.95rem;
  }
  .login-btn {
    font-size: 0.95rem;
    width: 80%;
  }
}
</style>
