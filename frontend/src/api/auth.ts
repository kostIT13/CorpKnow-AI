// src/api/auth.ts
import api from './client';
import type { LoginRequest, AuthTokens, User } from '../types';

export const authApi = {
  // 🔹 Логин
  login: async (data: LoginRequest): Promise<AuthTokens> => {
    const response = await api.post<AuthTokens>('/api/auth/login', data);
    return response.data;
  },

  // 🔹 Получить текущего пользователя
  me: async (): Promise<User> => {
    const response = await api.get<User>('/api/auth/me');
    return response.data;
  },

  // 🔹 Регистрация (если есть на бэкенде)
  register: async (data: LoginRequest & { name?: string }): Promise<AuthTokens> => {
    const response = await api.post<AuthTokens>('/api/auth/register', data);
    return response.data;
  },
};