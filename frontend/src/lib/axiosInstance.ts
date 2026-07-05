import axios from "axios";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8900",
  timeout: 30000, // 30 seconds, image analysis can take a moment
});

export default axiosInstance;
