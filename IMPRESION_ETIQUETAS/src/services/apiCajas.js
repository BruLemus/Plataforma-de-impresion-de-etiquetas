import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const crearCaja = async (cajaData) => {
  const response = await axios.post(`${API_URL}/cajas/`, cajaData);
  return response.data;
};

export const obtenerCajas = async () => {
  const response = await axios.get(`${API_URL}/cajas/`);
  return response.data;
};
