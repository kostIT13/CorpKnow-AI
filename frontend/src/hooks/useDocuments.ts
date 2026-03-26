// src/hooks/useDocuments.ts
import { useState, useCallback, useEffect } from 'react';
import { documentsApi } from '../api/documents';
import type { Document } from '../types';
import toast from 'react-hot-toast';

interface UseDocumentsReturn {
  documents: Document[];
  loading: boolean;
  uploading: boolean;
  loadDocuments: () => Promise<void>;
  uploadDocument: (file: File) => Promise<void>;
  deleteDocument: (id: string) => Promise<void>;
}

export function useDocuments(): UseDocumentsReturn {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  // 🔹 Загрузка документов при монтировании
  useEffect(() => {
    loadDocuments();
  }, []);

  // 🔹 Загрузка списка документов
  const loadDocuments = useCallback(async () => {
    setLoading(true);
    try {
      const docs = await documentsApi.list();
      setDocuments(docs);
    } catch (error) {
      toast.error('Не удалось загрузить документы');
    } finally {
      setLoading(false);
    }
  }, []);

  // 🔹 Загрузка файла
  const uploadDocument = useCallback(async (file: File) => {
    // 🔹 Валидация типа
    const allowedTypes = [
      'application/pdf',
      'text/plain',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ];
    
    if (!allowedTypes.includes(file.type)) {
      toast.error('Поддерживаются только PDF, TXT и DOCX файлы');
      throw new Error('Неподдерживаемый тип файла');
    }

    // 🔹 Валидация размера (10 МБ)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('Максимальный размер файла — 10 МБ');
      throw new Error('Файл слишком большой');
    }

    setUploading(true);
    const toastId = toast.loading('📤 Загрузка и обработка...');

    try {
      await documentsApi.upload(file);
      toast.success(`✅ ${file.name} загружен!`, { id: toastId });
      
      // 🔹 Обновляем список
      await loadDocuments();
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Ошибка при загрузке';
      toast.error(typeof message === 'string' ? message : 'Не удалось загрузить файл', { id: toastId });
      throw error;
    } finally {
      setUploading(false);
    }
  }, [loadDocuments]);

  // 🔹 Удаление документа
  const deleteDocument = useCallback(async (id: string) => {
    if (!confirm('Удалить этот документ?')) return;
    
    try {
      await documentsApi.delete(id);
      setDocuments(prev => prev.filter(d => d.id !== id));
      toast.success('Документ удалён');
    } catch (error) {
      toast.error('Ошибка при удалении документа');
    }
  }, []);

  return {
    documents,
    loading,
    uploading,
    loadDocuments,
    uploadDocument,
    deleteDocument,
  };
}