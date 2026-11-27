import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 120000,
});

export const getHealth = async () => {
  const response = await api.get("/health");
  return response.data;
};

export const getDetectionHistory = async () => {
  const response = await api.get("/api/detections");
  return response.data;
};

export const getVehicle = async (registration) => {
  const response = await api.get(
    `/api/vehicle/${registration}`
  );
  return response.data;
};

export const detectVehicle = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post(
    "/api/detect",
    formData
  );

  return response.data;
};

export default api;