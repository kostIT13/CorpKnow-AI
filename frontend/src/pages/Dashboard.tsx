// src/pages/Dashboard.tsx
import { useState, useEffect } from 'react';
import { Layout } from '../components/Layout';
import { authApi } from '../api/auth';
import type { User } from '../types';

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Получаем данные пользователя
    authApi.me()
      .then(setUser)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout userEmail={user?.email}>
      <div className="max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Добро пожаловать! 👋
        </h2>
        <p className="text-gray-600 mb-8">
          Загрузите документы и задавайте вопросы по их содержимому.
        </p>

        {/* Заглушки для следующих шагов */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">📤 Загрузить документ</h3>
            <p className="text-gray-500 text-sm">PDF, TXT, DOCX до 10 МБ</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">💬 Начать чат</h3>
            <p className="text-gray-500 text-sm">Задайте вопрос по документам</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}