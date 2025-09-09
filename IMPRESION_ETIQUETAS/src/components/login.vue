<template>
  <div class="login-wrapper">
    <div class="login-background">
      <div class="login-card">

        <!-- Título -->
        <h1 class="login-title">Bienvenido</h1>

        <!-- Carrusel -->
        <div class="carousel">
          <div
            class="carousel-slide"
            v-for="(img, idx) in carouselImages"
            :key="idx"
            v-show="currentSlide === idx"
          >
            <img :src="img" alt="Slide" />
          </div>
        </div>

        <!-- Formulario -->
        <input v-model="username" type="text" placeholder="Ingresa tu nombre" class="login-input" />
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
      carouselImages: [
        require("@/assets/e1.png"),
        require("@/assets/e2.png"),
        require("@/assets/e3.png"),
        require("@/assets/e4.png")
      ],
      currentSlide: 0,
    };
  },
  mounted() {
    setInterval(() => {
      this.currentSlide = (this.currentSlide + 1) % this.carouselImages.length;
    }, 3000);
  },
  methods: {
    login() {
      if (!this.username.trim()) return alert("Ingresa tu nombre");
      localStorage.setItem("username", this.username);
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
  background: linear-gradient(to right, #1e3a8a, #3b82f6);
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
  box-shadow: 0 12px 32px rgba(0,0,0,0.25);
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

/* Carrusel */
.carousel {
  height: 250px;
  margin-bottom: 30px;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.5s ease-in-out;
}

/* Input y botón */
.login-input {
  width: 90%;
  padding: 14px;
  margin-bottom: 20px;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 1.2rem;
}

.login-btn {
  width: 60%;
  padding: 14px;
  border-radius: 10px;
  border: none;
  background: #2563eb;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.3s;
}

.login-btn:hover {
  background: #1d4ed8;
}

/* ===== Media Queries ===== */
@media (max-width: 1024px) {
  .login-card {
    padding: 50px 30px;
  }
  .login-title {
    font-size: 2.5rem;
  }
  .carousel {
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
  .carousel {
    height: 180px;
  }
  .login-input {
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
  .carousel {
    height: 150px;
  }
  .login-input {
    font-size: 0.95rem;
  }
  .login-btn {
    font-size: 0.95rem;
    width: 80%;
  }
}
</style>
