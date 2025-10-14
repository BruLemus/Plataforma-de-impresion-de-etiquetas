<template>
  <div class="coordinador-dashboard">

    <!-- PERFIL COORDINADOR -->
    <section class="perfil-coordinador card">
      <h2>Mi Perfil</h2>
      <div class="perfil-info">
        <div class="sidebar-user" style="cursor:pointer;">
            <i class="fas fa-user-circle"></i>
            <span>{{ username }}</span>
        </div>
        <p><strong>Puesto:</strong> Coordinador</p>
      </div>
    </section>

    <!-- GESTIÓN DE PRACTICANTES -->
    <section class="practicantes card">
      <h2>Crear Usuarios</h2>
      <h1>-Practicantes-</h1>

      <!-- FORMULARIO CREAR PRACTICANTE -->
      <form @submit.prevent="crearPracticante" class="form-grid">
        <div class="form-field">
          <label>Nombre:</label>
          <input
            v-model="nuevoPracticante.nombre"
            type="text"
            required
            autocomplete="name"
          />
        </div>

        <div class="form-field password-field">
          <label>Contraseña:</label>
          <div class="password-wrapper">
            <input
              v-model="nuevoPracticante.contrasena"
              :type="mostrarContrasenaNuevo ? 'text' : 'password'"
              required
              autocomplete="new-password"
              placeholder="••••••"
            />
            <button type="button" class="toggle-btn" @click="mostrarContrasenaNuevo = !mostrarContrasenaNuevo">
              {{ mostrarContrasenaNuevo ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>

        <div class="form-field">
          <label>Mesa de trabajo:</label>
          <select v-model="nuevoPracticante.mesa_trabajo" class="login-select" required>
            <option disabled value="">Selecciona la mesa</option>
            <option v-for="n in 10" :key="n" :value="`MESA${n}`">MESA{{ n }}</option>
          </select>
        </div>

        <button type="submit" class="btn btn-save">Crear</button>
      </form>

      <!-- LISTA DE PRACTICANTES -->
      <h3>Practicantes Existentes</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Nombre</th>
              <th>Mesa Trabajo</th>
              <th>Contraseña</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, index) in practicantes" :key="p.user_id">
              <td>{{ index + 1 }}</td>
              <td><input v-model="p.nombre" autocomplete="name" /></td>
              <td>
                <select v-model="p.mesa_trabajo" class="login-select">
                  <option disabled value="">Selecciona la mesa</option>
                  <option v-for="n in 10" :key="n" :value="`MESA${n}`">MESA{{ n }}</option>
                </select>
              </td>
              <td class="password-field">
                <div class="password-wrapper">
                  <input
                    :type="p.mostrarContrasena ? 'text' : 'password'"
                    v-model="p.contrasena"
                    autocomplete="current-password"
                    placeholder="••••••"
                  />
                  <button type="button" class="toggle-btn" @click="p.mostrarContrasena = !p.mostrarContrasena">
                    {{ p.mostrarContrasena ? '🙈' : '👁️' }}
                  </button>
                </div>
              </td>
              <td class="actions">
                <button @click="editarPracticante(p)" class="btn btn-edit">Editar</button>
                <button @click="eliminarPracticante(p.user_id)" class="btn btn-delete">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </section>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";

export default {
  name: "DashboardCoordinador",
  setup() {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Debes iniciar sesión");
      window.location.href = "/login";
    }
    const headers = { Authorization: `Bearer ${token}` }; 

    const coordinador = ref({ nombre: "", user_id: "" });
    const username = localStorage.getItem("username") || "";

    const cargarPerfil = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/user_coordinadors_mx/perfil", { headers });
        coordinador.value.nombre = res.data?.nombre || "Nombre no disponible";
        coordinador.value.user_id = res.data?.user_id || "";
      } catch (error) {
        console.error("Error al cargar perfil:", error);
        coordinador.value.nombre = "Error al cargar";
        if (error.response?.status === 401) {
          alert("Token inválido o expirado");
          localStorage.removeItem("token");
          window.location.href = "/login";
        }
      }
    };

    const practicantes = ref([]);
    const nuevoPracticante = ref({ nombre: "", contrasena: "", mesa_trabajo: "" });
    const mostrarContrasenaNuevo = ref(false);

    const cargarPracticantes = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/user_practicantes_mx/", { headers });
        // 🔹 Ajuste: normalizamos mesa_trabajo para que siempre coincida con el Enum
        practicantes.value = res.data.map(p => ({
          ...p,
          contrasena: "",
          mostrarContrasena: false,
          mesa_trabajo: p.mesa_trabajo?.toUpperCase() || "" 
        }));
      } catch (error) {
        console.error("Error al cargar practicantes:", error);
      }
    };

    const crearPracticante = async () => {
      try {
        const payload = {
          ...nuevoPracticante.value,
          mesa_trabajo: nuevoPracticante.value.mesa_trabajo.toUpperCase() // 🔹 Ajuste
        };

        await axios.post("http://127.0.0.1:8000/user_practicantes_mx/", payload, { headers });
        alert("Practicante creado correctamente");

        // Limpiar formulario
        nuevoPracticante.value = { nombre: "", contrasena: "", mesa_trabajo: "" };
        await cargarPracticantes();
      } catch (error) {
        console.error("Error al crear practicante:", error);
        alert("Ocurrió un error al crear el practicante");
      }
    };

    const editarPracticante = async (p) => {
      try {
        const cambios = {
          nombre: p.nombre,
          contrasena: p.contrasena || undefined,
          mesa_trabajo: p.mesa_trabajo.toUpperCase() // 🔹 Ajuste
        };
        await axios.put(`http://127.0.0.1:8000/user_practicantes_mx/${p.user_id}`, cambios, { headers });
        alert(`Practicante "${p.nombre}" actualizado correctamente`);
        await cargarPracticantes();
      } catch (error) {
        console.error("Error al editar practicante:", error);
        alert("Ocurrió un error al editar el practicante");
      }
    };

    const eliminarPracticante = async (id) => {
      if (!confirm("¿Deseas eliminar este practicante?")) return;

      try {
        await axios.delete(`http://127.0.0.1:8000/user_practicantes_mx/${id}`, { headers });
        practicantes.value = practicantes.value.filter(p => p.user_id !== id);
        alert("Practicante eliminado correctamente");
      } catch (error) {
        console.error("Error al eliminar practicante:", error);
        alert("Ocurrió un error al eliminar el practicante");
      }
    };

    onMounted(() => {
      cargarPerfil();
      cargarPracticantes();
    });

    return {
      username,
      coordinador,
      practicantes,
      nuevoPracticante,
      mostrarContrasenaNuevo,
      crearPracticante,
      editarPracticante,
      eliminarPracticante
    };
  }
};
</script>





<style scoped>
.coordinador-dashboard {
  max-width: 1000px;
  margin: 20px auto;
  padding: 20px;
  font-family: 'Poppins', sans-serif;
  color: #1f2937;
}

.card {
  text-align: center;
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.05);
  margin-bottom: 30px;
}

.perfil-info p {
  font-size: 1rem;
  margin-bottom: 10px;
  color: #1e3a8a;
}

.btn {
  padding: 12px 20px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: #fff;
  border: none;
}

.btn-save { background: #2563eb; }
.btn-save:hover { background: #1d4ed8; }
.btn-edit { background: #fbbf24; color: #1f2937; }
.btn-edit:hover { background: #f59e0b; }
.btn-delete { background: #ef4444; }
.btn-delete:hover { background: #dc2626; }

.table-wrapper { overflow-x: auto; margin-top: 15px; }
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  text-align: left;
  font-size: 0.95rem;
}
th {
  background: #f3f4f6;
  font-weight: 600;
  color: #111827;
}
tr:nth-child(even) { background: #f9fafb; }
tr:hover { background: #e0f2fe; transition: background 0.2s; }
.actions button { margin-right: 5px; }

h2 { font-size: 1.8rem; font-weight: 700; color: #2563eb; margin-bottom: 15px; }
h3 { font-size: 1.3rem; font-weight: 600; margin: 15px 0; color: #1e40af; }

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 15px;
  align-items: end;
}

.form-field {
  display: flex;
  flex-direction: column;
}
.form-field label {
  font-weight: 600;
  margin-bottom: 6px;
  color: #1e3a8a;
}
input, select {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  font-size: 0.95rem;
  transition: all 0.2s;
  background: #f9fafb;
}
input:focus, select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.2);
}

.password-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-wrapper input {
  width: 100%;
  padding-right: 40px; /* espacio para el botón dentro del input */
  box-sizing: border-box;
}

.toggle-btn {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #6b7280;
}


@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
}
</style>
