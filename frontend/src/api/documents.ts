import api from './client';
import type { Document } from '../types';

export const documentsApi = {
  list: async (): Promise<Document[]> => {
    const response = await api.get<Document[]>('/api/documents/');
    return response.data;
  },

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

  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/documents/${id}`);
  },

  get: async (id: string): Promise<Document> => {
    const response = await api.get<Document>(`/api/documents/${id}`);
    return response.data;
  },
};