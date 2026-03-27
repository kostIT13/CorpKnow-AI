import { useEffect, useState } from 'react';
import { chatApi } from '../../api/chat';
import type { ChatSession } from '../../types';
import toast from 'react-hot-toast';

interface ChatSidebarProps {
  currentChatId: string | null;
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void;
}

export default function ChatSidebar({ currentChatId, onSelectChat, onNewChat }: ChatSidebarProps) {
  const [chats, setChats] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadChats();
  }, []);

  const loadChats = async () => {
    try {
      const chatList = await chatApi.listChats();
      setChats(chatList);
    } catch (error) {
      console.error('Failed to load chats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (e: React.MouseEvent, chatId: string) => {
    e.stopPropagation();
    if (!confirm('Удалить этот чат?')) return;
    
    try {
      await chatApi.deleteChat(chatId);
      setChats(prev => prev.filter(c => c.id !== chatId && c.chat_id !== chatId));
      toast.success('Чат удалён');
    } catch (error) {
      toast.error('Ошибка при удалении');
    }
  };

  const formatTitle = (title: string) => {
    return title || 'Новый чат';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
    });
  };

  return (
    <aside className="w-64 bg-gray-900 text-white flex flex-col h-full">
      <div className="p-4 border-b border-gray-800">
        <button
          onClick={onNewChat}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition flex items-center justify-center gap-2 font-medium"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Новый чат
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {loading ? (
          <div className="text-center py-4 text-gray-400 text-sm">Загрузка...</div>
        ) : chats.length === 0 ? (
          <div className="text-center py-8 text-gray-400 text-sm">
            <p>Нет чатов</p>
            <p className="text-xs mt-1">Создайте первый чат</p>
          </div>
        ) : (
          chats.map(chat => {
            const chatId = chat.chat_id || chat.id;

            if (!chatId) return null;

            const isActive = currentChatId === chatId;
            
            return (
              <div
                key={chatId}
                onClick={() => onSelectChat(chatId)}
                className={`group px-3 py-3 rounded-lg cursor-pointer transition flex items-center justify-between ${
                  isActive
                    ? 'bg-blue-600 hover:bg-blue-700'
                    : 'hover:bg-gray-800'
                }`}
              >
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium truncate">
                    {formatTitle(chat.title)}
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {formatDate(chat.updated_at)}
                  </p>
                </div>
                
                <button
                  onClick={(e) => handleDelete(e, chatId)}
                  className={`p-1 rounded transition ${
                    isActive 
                      ? 'opacity-100 hover:bg-red-500' 
                      : 'opacity-0 group-hover:opacity-100 hover:bg-red-500'
                  }`}
                  title="Удалить чат"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
}