// src/api/chat.ts
import api from './client';
import type { ChatRequest, ChatResponse } from '../types';

export const chatApi = {
  // 🔹 Отправить вопрос и получить ответ
  completion: async (data: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/api/chat/completions', data);
    return response.data;
  },

  // 🔹 Получить историю чата (если есть на бэкенде)
  history: async (chatId?: string): Promise<any> => {
    const url = chatId ? `/api/chat/${chatId}/history` : '/api/chat/history';
    const response = await api.get(url);
    return response.data;
  },
};