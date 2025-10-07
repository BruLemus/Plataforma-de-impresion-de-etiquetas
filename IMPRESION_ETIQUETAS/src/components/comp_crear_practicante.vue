<template>
  <div class="coordinador-dashboard">

    <!-- PERFIL COORDINADOR -->
    <section class="perfil-coordinador card">
      <h2>Mi Perfil</h2>
      <form @submit.prevent="actualizarPerfil" class="form-grid">
        <div class="form-field">
          <label>Nombre:</label>
          <input v-model="coordinador.nombre" type="text" required autocomplete="name" />
        </div>

        <div class="form-field password-field">
          <label>Contraseña:</label>
          <div class="password-wrapper">
            <input
              v-model="coordinador.contrasena"
              :type="mostrarContrasenaCoord ? 'text' : 'password'"
              autocomplete="new-password"
            />
            <button
              type="button"
              class="toggle-btn"
              @click="mostrarContrasenaCoord = !mostrarContrasenaCoord"
            >
              {{ mostrarContrasenaCoord ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>

        <div class="form-field">
          <label>Código Secreto:</label>
          <input
            v-model="coordinador.codigo_secreto"
            type="text"
            autocomplete="off"
            required
          />
        </div>

        <button type="submit" class="btn btn-save">Actualizar Perfil</button>
      </form>

      <!-- ELIMINAR PERFIL DEL COORDINADOR -->
      <button
        @click="eliminarPerfil"
        class="btn btn-delete"
        style="margin-top: 15px;"
      >
        Eliminar mi cuenta
      </button>
    </section>

    <hr />

    <!-- GESTIÓN DE PRACTICANTES -->
    <section class="practicantes card">
      <h2>Gestión de Practicantes</h2>

      <!-- Crear Practicante -->
      <form @submit.prevent="crearPracticante" class="form-grid">
        <h3>Crear Practicante</h3>
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
            />
            <button
              type="button"
              class="toggle-btn"
              @click="mostrarContrasenaNuevo = !mostrarContrasenaNuevo"
            >
              {{ mostrarContrasenaNuevo ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>

        <div class="form-field">
          <label>Mesa de trabajo:</label>
          <select v-model="nuevoPracticante.mesa_trabajo" class="login-select" required>
            <option disabled value="">Selecciona la mesa</option>
            <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
          </select>
        </div>

        <button type="submit" class="btn btn-save">Crear</button>
      </form>

      <!-- Lista de Practicantes -->
      <h3>Practicantes Existentes</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Mesa Trabajo</th>
              <th>Contraseña</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in practicantes" :key="p.user_id">
              <td>{{ p.user_id }}</td>
              <td><input v-model="p.nombre" autocomplete="name" /></td>
              <td>
                <select v-model="p.mesa_trabajo" class="login-select">
                  <option disabled value="">Selecciona la mesa</option>
                  <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
                </select>
              </td>
              <td class="password-field">
                <div class="password-wrapper">
                  <input
                    :type="p.mostrarContrasena ? 'text' : 'password'"
                    v-model="p.contrasena"
                    autocomplete="current-password"
                  />
                  <button
                    type="button"
                    class="toggle-btn"
                    @click="p.mostrarContrasena = !p.mostrarContrasena"
                  >
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
    // Obtener token del localStorage
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Debes iniciar sesión");
      window.location.href = "/login";
    }
    const headers = { Authorization: `Bearer ${token}` };

    // ---------------------------
    // PERFIL COORDINADOR
    // ---------------------------
    const coordinador = ref({ nombre: "", contrasena: "", codigo_secreto: "", user_id: "" });
    const mostrarContrasenaCoord = ref(false);

    const cargarPerfil = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/user_coordinadors/perfil", { headers });
        coordinador.value = res.data;
      } catch (error) {
        console.error("Error al cargar perfil:", error);
        if (error.response && error.response.status === 401) {
          alert("Token inválido o expirado");
          localStorage.removeItem("token");
          window.location.href = "/login";
        }
      }
    };

    const actualizarPerfil = async () => {
      if (!coordinador.value.codigo_secreto) {
        alert("Debes ingresar tu código secreto para actualizar el perfil");
        return;
      }

      try {
        const payload = {
          nombre: coordinador.value.nombre,
          contrasena: coordinador.value.contrasena,
          codigo_secreto: coordinador.value.codigo_secreto
        };

        await axios.put(
          "http://127.0.0.1:8000/user_coordinadors/perfil",
          payload,
          { headers }
        );

        alert("Perfil actualizado correctamente");
        coordinador.value.contrasena = "";
      } catch (error) {
        if (error.response && error.response.status === 403) {
          alert("Código secreto incorrecto");
        } else if (error.response && error.response.status === 401) {
          alert("Token inválido o expirado");
          localStorage.removeItem("token");
          window.location.href = "/login";
        } else {
          console.error("Error al actualizar perfil:", error);
          alert("Error al actualizar perfil");
        }
      }
    };

    const eliminarPerfil = async () => {
      if (!confirm("¿Deseas eliminar tu cuenta?")) return;
      try {
        await axios.delete(`http://127.0.0.1:8000/user_coordinadors/${coordinador.value.user_id}`, { headers });
        alert("Cuenta eliminada correctamente");
        localStorage.removeItem("token");
        window.location.href = "/login";
      } catch (error) {
        console.error("Error al eliminar cuenta:", error);
        alert("No se pudo eliminar la cuenta");
      }
    };

    // ---------------------------
    // GESTIÓN DE PRACTICANTES
    // ---------------------------
    const practicantes = ref([]);
    const nuevoPracticante = ref({ nombre: "", contrasena: "", mesa_trabajo: "" });
    const mostrarContrasenaNuevo = ref(false);

    const cargarPracticantes = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/user_practicantes/", { headers });
        practicantes.value = res.data.map((p) => ({ ...p, contrasena: "", mostrarContrasena: false }));
      } catch (error) {
        console.error("Error al cargar practicantes:", error);
      }
    };

    const crearPracticante = async () => {
      try {
        await axios.post("http://127.0.0.1:8000/user_practicantes/", nuevoPracticante.value, { headers });
        alert("Practicante creado correctamente");
        nuevoPracticante.value = { nombre: "", contrasena: "", mesa_trabajo: "" };
        await cargarPracticantes();
      } catch (error) {
        console.error("Error al crear practicante:", error);
      }
    };

    const editarPracticante = async (p) => {
      try {
        await axios.put(`http://127.0.0.1:8000/user_practicantes/${p.user_id}`, p, { headers });
        alert("Practicante actualizado correctamente");
        await cargarPracticantes();
      } catch (error) {
        console.error("Error al editar practicante:", error);
      }
    };

    const eliminarPracticante = async (id) => {
      if (!confirm("¿Deseas eliminar este practicante?")) return;
      try {
        await axios.delete(`http://127.0.0.1:8000/user_practicantes/${id}`, { headers });
        alert("Practicante eliminado correctamente");
        await cargarPracticantes();
      } catch (error) {
        console.error("Error al eliminar practicante:", error);
      }
    };

    // ---------------------------
    // ON MOUNT
    // ---------------------------
    onMounted(() => {
      cargarPerfil();
      cargarPracticantes();
    });

    return {
      coordinador,
      mostrarContrasenaCoord,
      actualizarPerfil,
      eliminarPerfil,
      practicantes,
      nuevoPracticante,
      mostrarContrasenaNuevo,
      crearPracticante,
      editarPracticante,
      eliminarPracticante,
    };
  },
};
</script>


<style scoped>
/* Mantengo tus estilos existentes */
.coordinador-dashboard {
  max-width: 950px;
  margin: 20px auto;
  padding: 20px;
  font-family: 'Poppins', sans-serif;
  color: #1f2937;
}

.card {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.05);
  margin-bottom: 30px;
}

.password-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.password-wrapper input {
  flex: 1;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  margin-left: 8px;
}

h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2563eb;
  margin-bottom: 20px;
}

h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 15px 0;
  color: #1e40af;
}

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
}

input:focus, select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 5px rgba(37, 99, 235, 0.3);
}

.btn {
  padding: 10px 18px;
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

.table-wrapper { overflow-x: auto; }
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
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
.actions button { margin-right: 5px; }

@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
}
</style>
