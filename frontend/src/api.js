import axios from 'axios';

const { protocol, hostname } = window.location;
const api = axios.create({
  baseURL: `${protocol}//${hostname}:5000`,  // coges http(s) y host actuales
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;

