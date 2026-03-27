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

  useEffect(() => {
    if (!initialized.current) {
      loadChats();
      initialized.current = true;
    }
  }, []);

  const loadChats = useCallback(async () => {
    try {
      const chatList = await chatApi.listChats();
      setChats(chatList);
      
      if (chatList.length > 0 && !currentChatId) {
        const firstChatId = chatList[0].chat_id || chatList[0].id;
        if (firstChatId) {
          await selectChat(firstChatId);
        }
      }
    } catch (error: any) {
      console.error('Ошибка загрузки чатов:', error);
      toast.error('Не удалось загрузить чаты');
    } finally {
      setLoading(false);
    }
  }, [currentChatId]);

  const selectChat = useCallback(async (chatId: string) => {
    setSending(true);
    try {
      const history: ChatHistory = await chatApi.getHistory(chatId);
      setCurrentChatId(chatId);
      
      setMessages(history.messages.map(msg => ({
        id: msg.id,
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
        sources: msg.sources || [], 
        created_at: msg.created_at,
        is_starred: msg.is_starred,
      })));
    } catch (error: any) {
      console.error('Ошибка загрузки истории:', {
        message: error.message,
        status: error.response?.status,
        data: error.response?.data,
        chatId,
      });
      
      if (error.response?.status === 404) {
        setMessages([]);
        setCurrentChatId(chatId);
        return;
      }
      
      toast.error('Не удалось загрузить историю чата');
    } finally {
      setSending(false);
    }
  }, []);

  const createNewChat = useCallback(async () => {
    try {
      const newChat = await chatApi.createChat();
      setChats(prev => [newChat, ...prev]);
      const chatId = newChat.chat_id || newChat.id || '';
      setCurrentChatId(chatId);  
      setMessages([]);
      toast.success('Новый чат создан');
    } catch (error: any) {
      console.error('Ошибка создания чата:', error);
      toast.error('Не удалось создать чат');
    }
  }, []);

  const sendMessage = useCallback(async (query: string) => {
    if (!query.trim()) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: query,
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMsg]);
    setSending(true);

    try {
      const response = await chatApi.completion({
        query,
        chat_id: currentChatId || undefined,
      });

      if (!currentChatId && response.chat_id) {
        setCurrentChatId(response.chat_id);
        await loadChats();
      }

      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.content,
        sources: response.sources || [],
        created_at: response.created_at,
      };
      setMessages(prev => [...prev, assistantMsg]);

    } catch (error: any) {
      const message = error.response?.data?.detail || 'Ошибка при получении ответа';
      toast.error(typeof message === 'string' ? message : 'Не удалось получить ответ');
      
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

  const deleteChat = useCallback(async (chatId: string) => {
    if (!confirm('Удалить этот чат?')) return;
    
    try {
      await chatApi.deleteChat(chatId);
      setChats(prev => prev.filter(c => (c.chat_id || c.id) !== chatId));
      
      if (currentChatId === chatId) {
        setCurrentChatId(null);
        setMessages([]);
      }
      
      toast.success('Чат удалён');
    } catch (error: any) {
      console.error('Ошибка удаления чата:', error);
      toast.error('Ошибка при удалении чата');
    }
  }, [currentChatId]);

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