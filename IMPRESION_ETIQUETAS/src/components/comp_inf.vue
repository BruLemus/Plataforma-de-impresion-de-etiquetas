<!-- src/components/AcercaDelDesarrollador.vue -->
<template>
  <div class="app-container">
    <!-- HEADER -->
    <header class="header no-print">
      <div class="header-content">
        <h1 class="logo">💻 Acerca del Desarrollador</h1>
      </div>
    </header>

    <!-- TARJETA DE DESARROLLADOR -->
    <div class="developer-card">
      <div class="developer-info">
        <h2>{{ desarrollador.nombre }}</h2>
        <p><strong></strong> {{ desarrollador.rol }}</p>
        <p><strong>Correo:</strong> <a :href="'mailto:' + desarrollador.correo">{{ desarrollador.correo }}</a></p>
        <p><strong>GitHub:</strong> <a :href="desarrollador.github" target="_blank">{{ desarrollador.github }}</a></p>
        <p><strong>Descripción:</strong> {{ desarrollador.descripcion }}</p>
      </div>
      <div class="developer-skills">
        <h3>Contribuciones y habilidades:</h3>
        <ul>
          <li v-for="(habilidad, index) in desarrollador.habilidades" :key="index">
            {{ habilidad }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AcercaDelDesarrollador",
  data() {
    return {
      desarrollador: {
        nombre: "Bruno Lemus Gonzalez",
        rol: "Ingeniero en Desarrollo y Gestión de Software",
        correo: "brno.lems@gmail.com",
        github: "https://github.com/BruLemus",
        descripcion:
          "Creador de esta aplicación, responsable del diseño, implementación y optimización de todas las funcionalidades. " +
          "Se implementaron módulos de gestión de datos, autenticación con JWT, componentes dinámicos y escalabilidad para el futuro.",
        habilidades: [
          "Diseño y desarrollo de interfaces Vue.js",
          "Integración con APIs REST y FastAPI",
          "Implementación de autenticación con JWT",
          "Diseño de bases de datos relacionales y no relacionales",
          "Gestión de estados y componentes dinámicos",
          "Optimización de rendimiento y escalabilidad",
          "Pruebas unitarias y buenas prácticas de desarrollo",
        ],
      },
    };
  },
};
</script>

<style scoped>
.app-container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  background: #333;
  color: white;
  padding: 15px;
  margin-bottom: 20px;
}

.logo {
  margin: 0;
}

.developer-card {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 1px 1px 8px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.developer-info h2 {
  margin: 0 0 5px 0;
  color: #333;
}

.developer-info p {
  margin: 3px 0;
}

.developer-info a {
  color: #007bff;
  text-decoration: none;
}

.developer-skills h3 {
  margin-bottom: 8px;
}

.developer-skills ul {
  list-style-type: disc;
  padding-left: 20px;
}

.developer-skills li {
  margin-bottom: 5px;
}
</style>
