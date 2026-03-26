// src/api/documents.ts
import api from './client';
import type { Document } from '../types';

export const documentsApi = {
  // 🔹 Список документов
  list: async (): Promise<Document[]> => {
    const response = await api.get<Document[]>('/api/documents/');
    return response.data;
  },

  // 🔹 Загрузка файла
  upload: async (file: File): Promise<Document> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<Document>('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // 🔹 Удаление документа
  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/documents/${id}`);
  },

  // 🔹 Получить документ по ID
  get: async (id: string): Promise<Document> => {
    const response = await api.get<Document>(`/api/documents/${id}`);
    return response.data;
  },
};