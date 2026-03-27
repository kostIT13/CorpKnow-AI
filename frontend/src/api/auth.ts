import api from './client';
import type { LoginRequest, AuthTokens, User } from '../types';

export const authApi = {
  login: async (data: LoginRequest): Promise<AuthTokens> => {
    const response = await api.post<AuthTokens>('/api/auth/login', data);
    return response.data;
  },

  register: async (data: LoginRequest & { name?: string }): Promise<AuthTokens> => {
    const response = await api.post<AuthTokens>('/api/auth/register', data);
    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await api.get<User>('/api/auth/me');
    return response.data;
  },
};