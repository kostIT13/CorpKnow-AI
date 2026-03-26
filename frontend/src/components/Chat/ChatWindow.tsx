// src/components/Chat/ChatWindow.tsx
import { useState, useRef, useEffect } from 'react';
import { chatApi } from '../../api/chat';
import  MessageBubble  from './MessageBubble';
import  ChatInput  from './ChatInput';
import  SourceCard  from './SourceCard';
import type { Message, ChatResponse } from '../../types';
import toast from 'react-hot-toast';

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  // 🔹 Авто-скролл вниз при новом сообщении
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (query: string) => {
    // 🔹 Добавляем сообщение пользователя
    const userMsg: Message = { role: 'user', content: query };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);
    setSources([]);

    try {
      // 🔹 Запрос к RAG API
      const response: ChatResponse = await chatApi.completion({ query });
      
      // 🔹 Добавляем ответ ассистента
      const assistantMsg: Message = {
        role: 'assistant',
        content: response.content,
        sources: response.sources,
        created_at: response.created_at,
      };
      setMessages(prev => [...prev, assistantMsg]);
      setSources(response.sources || []);
      
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Ошибка при получении ответа';
      toast.error(typeof message === 'string' ? message : 'Не удалось получить ответ');
      
      // 🔹 Добавляем сообщение об ошибке
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '❌ Произошла ошибка. Попробуйте позже.',
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Заголовок */}
      <div className="border-b border-gray-200 pb-4 mb-4">
        <h2 className="text-xl font-semibold text-gray-900">💬 Чат с документами</h2>
        <p className="text-sm text-gray-500 mt-1">
          Задавайте вопросы по загруженным документам
        </p>
      </div>

      {/* Сообщения */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.length === 0 ? (
          /* Пустое состояние */
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🤖</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900">Начните диалог</h3>
            <p className="text-gray-500 mt-1">
              Задайте вопрос по вашим документам
            </p>
            <div className="mt-6 flex flex-wrap gap-2 justify-center">
              {['О чём этот документ?', 'Сколько дней отпуска?', 'Как оформить больничный?'].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => handleSend(suggestion)}
                  className="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm text-gray-600 hover:border-blue-400 hover:text-blue-600 transition"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : (
          /* Список сообщений */
          <>
            {messages.map((msg, i) => (
              <MessageBubble key={i} message={msg} />
            ))}
            
            {/* Индикатор загрузки */}
            {loading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-green-600 flex items-center justify-center">
                  <span className="text-white text-sm">🤖</span>
                </div>
                <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={scrollRef} />
          </>
        )}
      </div>

      {/* Источники */}
      {sources.length > 0 && (
        <div className="border-t border-gray-200 pt-4 mb-4">
          <p className="text-sm text-gray-500 mb-2">📚 Источники:</p>
          <div className="flex flex-wrap gap-2">
            {sources.map((src, i) => (
              <SourceCard key={i} filename={src} />
            ))}
          </div>
        </div>
      )}

      {/* Поле ввода */}
      <ChatInput onSend={handleSend} disabled={loading} />
    </div>
  );
}