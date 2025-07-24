import axios from 'axios';

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000' });
API.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export async function login(data) {
  const res = await API.post('/auth/login', data);
  localStorage.setItem('token', res.data.access_token);
  return res;
}

export async function fetchYieldData() {
  const res = await API.get('/analytics/yield');
  return res.data;
}

export async function fetchWaferMap(id) {
  const res = await API.get(`/analytics/wafer_map/${id}`);
  return res.data;
}
