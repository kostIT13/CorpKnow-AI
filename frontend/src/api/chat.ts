import api from './client';

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
  completion: async (data: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/api/chat/completions', data);
    return response.data;
  },

  getHistory: async (chatId: string): Promise<ChatHistory> => {
    const response = await api.get<ChatHistory>(`/api/chat/history/${chatId}`);
    if (response.data.messages) {
      response.data.messages = response.data.messages.map((msg: any) => ({
        ...msg,
        sources: msg.sources || [],
      }));
    }
    return response.data;
  },

  listChats: async (): Promise<ChatSession[]> => {
    const response = await api.get<ChatSession[]>('/api/chats/');
    return response.data;
  },

  createChat: async (title?: string): Promise<ChatSession> => {
    const response = await api.post<ChatSession>('/api/chats/', { title });
    return response.data;
  },

  deleteChat: async (chatId: string): Promise<void> => {
    await api.delete(`/api/chats/${chatId}`);
  },

  updateTitle: async (chatId: string, title: string): Promise<ChatSession> => {
    const response = await api.patch<ChatSession>(`/api/chats/${chatId}`, { title });
    return response.data;
  },
};