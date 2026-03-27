import { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import SourceCard from './SourceCard';
import {useChat} from '../../hooks'; 
import type { Message } from '../../types';

export default function ChatWindow() {
  const {
    messages,
    sending,
    sendMessage,
    createNewChat,
  } = useChat();
  
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const handleSend = async (query: string) => {
    await sendMessage(query);
  };

  const handleNewChat = async () => {
    await createNewChat();
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      <div className="border-b border-gray-200 pb-4 mb-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">💬 Чат с документами</h2>
            <p className="text-sm text-gray-500 mt-1">
              Задавайте вопросы по загруженным документам
            </p>
          </div>
          
          <button
            onClick={handleNewChat}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition flex items-center gap-2 text-sm font-medium"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Новый чат
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.length === 0 ? (
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
          <>
            {messages.map((msg: Message, i: number) => (  
              <MessageBubble key={msg.id || i} message={msg} />
            ))}
            
            {sending && (
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

      {messages.length > 0 && messages[messages.length - 1].sources && messages[messages.length - 1].sources!.length > 0 && (
        <div className="border-t border-gray-200 pt-4 mb-4">
          <p className="text-sm text-gray-500 mb-2">📚 Источники:</p>
          <div className="flex flex-wrap gap-2">
            {messages[messages.length - 1].sources!.map((src: string, i: number) => (
              <SourceCard key={i} filename={src} />
            ))}
          </div>
        </div>
      )}

      <ChatInput onSend={handleSend} disabled={sending} />
    </div>
  );
}