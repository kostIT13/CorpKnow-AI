// src/hooks/useAuth.ts
import { useState, useEffect, useCallback } from 'react';
import { authApi } from '../api/auth';
import type { User, LoginRequest } from '../types';
import toast from 'react-hot-toast';

interface UseAuthReturn {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (data: LoginRequest) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // 🔹 Проверка авторизации при загрузке
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = useCallback(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      const userData = await authApi.me();
      setUser(userData);
    } catch (error) {
      // Токен невалиден
      localStorage.removeItem('token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  // 🔹 Логин
  const login = async (data: LoginRequest) => {
    setLoading(true);
    try {
      const tokens = await authApi.login(data);
      localStorage.setItem('token', tokens.access_token);
      
      const userData = await authApi.me();
      setUser(userData);
      
      toast.success('✅ Успешный вход!');
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Ошибка при входе';
      toast.error(typeof message === 'string' ? message : 'Неверный email или пароль');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // 🔹 Логаут
  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setUser(null);
    toast.success('Вы вышли из системы');
  }, []);

  return {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
    checkAuth,
  };
}