import { useState, useCallback, useRef, useEffect } from 'react';
import { chatApi } from '../api/chat';
import type { Message, ChatSession, ChatHistory } from '../types';
import toast from 'react-hot-toast';

interface UseChatReturn {
  messages: Message[];
  chats: ChatSession[];
  currentChatId: string | null;
  loading: boolean;
  sending: boolean;
  loadChats: () => Promise<void>;
  selectChat: (chatId: string) => Promise<void>;
  createNewChat: () => Promise<void>;
  sendMessage: (query: string) => Promise<void>;
  deleteChat: (chatId: string) => Promise<void>;
  clearMessages: () => void;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [chats, setChats] = useState<ChatSession[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  
  const initialized = useRef(false);

  // 🔹 Загрузка чатов при монтировании
  useEffect(() => {
    if (!initialized.current) {
      loadChats();
      initialized.current = true;
    }
  }, []);

  // 🔹 Загрузка списка чатов
  const loadChats = useCallback(async () => {
    try {
      const chatList = await chatApi.listChats();
      setChats(chatList);
      
      // Если есть чаты, загружаем последний
      if (chatList.length > 0 && !currentChatId) {
        await selectChat(chatList[0].chat_id);
      }
    } catch (error) {
      toast.error('Не удалось загрузить чаты');
    } finally {
      setLoading(false);
    }
  }, [currentChatId]);

  // 🔹 Выбор чата
  const selectChat = useCallback(async (chatId: string) => {
    setSending(true);
    try {
      const history: ChatHistory = await chatApi.getHistory(chatId);
      setCurrentChatId(chatId);
      
      // Конвертируем историю в сообщения
      setMessages(history.messages.map(msg => ({
        id: msg.id,
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
        sources: msg.sources,
        created_at: msg.created_at,
        is_starred: msg.is_starred,
      })));
    } catch (error) {
      toast.error('Не удалось загрузить историю чата');
    } finally {
      setSending(false);
    }
  }, []);

  // 🔹 Создание нового чата
  const createNewChat = useCallback(async () => {
    try {
      const newChat = await chatApi.createChat();
      setChats(prev => [newChat, ...prev]);
      setCurrentChatId(newChat.chat_id);
      setMessages([]);
      toast.success('Новый чат создан');
    } catch (error) {
      toast.error('Не удалось создать чат');
    }
  }, []);

  // 🔹 Отправка сообщения
  const sendMessage = useCallback(async (query: string) => {
    if (!query.trim()) return;

    // 🔹 Добавляем сообщение пользователя
    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: query,
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMsg]);
    setSending(true);

    try {
      // 🔹 Запрос к API
      const response = await chatApi.completion({
        query,
        chat_id: currentChatId || undefined,
      });

      // 🔹 Если это первое сообщение, обновляем currentChatId
      if (!currentChatId && response.chat_id) {
        setCurrentChatId(response.chat_id);
        // Обновляем список чатов
        await loadChats();
      }

      // 🔹 Добавляем ответ ассистента
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.content,
        sources: response.sources,
        created_at: response.created_at,
      };
      setMessages(prev => [...prev, assistantMsg]);

    } catch (error: any) {
      const message = error.response?.data?.detail || 'Ошибка при получении ответа';
      toast.error(typeof message === 'string' ? message : 'Не удалось получить ответ');
      
      // 🔹 Добавляем сообщение об ошибке
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '❌ Произошла ошибка. Попробуйте позже.',
        created_at: new Date().toISOString(),
      }]);
    } finally {
      setSending(false);
    }
  }, [currentChatId, loadChats]);

  // 🔹 Удаление чата
  const deleteChat = useCallback(async (chatId: string) => {
    if (!confirm('Удалить этот чат?')) return;
    
    try {
      await chatApi.deleteChat(chatId);
      setChats(prev => prev.filter(c => c.chat_id !== chatId));
      
      if (currentChatId === chatId) {
        setCurrentChatId(null);
        setMessages([]);
      }
      
      toast.success('Чат удалён');
    } catch (error) {
      toast.error('Ошибка при удалении чата');
    }
  }, [currentChatId]);

  // 🔹 Очистка сообщений
  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    chats,
    currentChatId,
    loading,
    sending,
    loadChats,
    selectChat,
    createNewChat,
    sendMessage,
    deleteChat,
    clearMessages,
  };
}