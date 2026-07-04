import axios from 'axios';

export const API_BASE = import.meta.env.VITE_API_BASE ?? (import.meta.env.DEV ? 'http://localhost:8000' : '');

export const api = axios.create({
  baseURL: `${API_BASE}/api`,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export function mediaUrl(path: string | null): string | null {
  if (!path) return null;
  const normalized = path.replace('../uploads', '/uploads').replace('uploads', '/uploads');
  return `${API_BASE}${normalized}`;
}
