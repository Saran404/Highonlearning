import type { LoginResponse, User } from '../types';
import { api } from './client';

export const authApi = {
  register: (body: { name: string; email: string; password: string }) =>
    api.post<{ user: User }>('/auth/register', body).then((r) => r.data),
  login: (body: { email: string; password: string; device_id: string }) =>
    api.post<LoginResponse>('/auth/login', body).then((r) => r.data),
  logout: () => api.post('/auth/logout').then((r) => r.data),
  me: () => api.get<User>('/auth/me').then((r) => r.data),
  sessions: () => api.get('/auth/sessions').then((r) => r.data),
};
