// src/pages/Dashboard.tsx
import { useState, useEffect } from 'react';
import { Layout } from '../components/Layout';
import { ChatWindow } from '../components/Chat';
import { authApi } from '../api/auth';
import type { User } from '../types';

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
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
      <ChatWindow />
    </Layout>
  );
}