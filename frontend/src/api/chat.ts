// src/api/chat.ts
import api from './client';

// 🔹 Правильный путь к types (на уровень выше → types/index.ts)
import type { ChatRequest, ChatResponse, ChatSession, ChatHistory } from '../types';

export interface MessageResponse {
  id: string;
  role: string;
  content: string,
  sources: string[];
  created_at: string;
  is_starred: boolean;
}

export const chatApi = {
  // 🔹 Отправить вопрос и получить ответ
  completion: async (data: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/api/chat/completions', data);
    return response.data;
  },

  // 🔹 Получить историю чата
  getHistory: async (chatId: string): Promise<ChatHistory> => {
    const response = await api.get<ChatHistory>(`/api/chat/history/${chatId}`);
  // 🔹 Гарантируем, что sources всегда массив
    if (response.data.messages) {
      response.data.messages = response.data.messages.map((msg: any) => ({
        ...msg,
        sources: msg.sources || [],
      }));
    }
    return response.data;
  },

  // 🔹 Получить список всех чатов
  listChats: async (): Promise<ChatSession[]> => {
    const response = await api.get<ChatSession[]>('/api/chats/');
    return response.data;
  },

  // 🔹 Создать новый чат
  createChat: async (title?: string): Promise<ChatSession> => {
    const response = await api.post<ChatSession>('/api/chats/', { title });
    return response.data;
  },

  // 🔹 Удалить чат
  deleteChat: async (chatId: string): Promise<void> => {
    await api.delete(`/api/chats/${chatId}`);
  },

  // 🔹 Обновить заголовок чата
  updateTitle: async (chatId: string, title: string): Promise<ChatSession> => {
    const response = await api.patch<ChatSession>(`/api/chats/${chatId}`, { title });
    return response.data;
  },
};