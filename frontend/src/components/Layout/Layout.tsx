import type { ReactNode } from 'react';
import { Header, Sidebar } from './index';

interface LayoutProps {
  children: ReactNode;
  userEmail?: string;
}

export default function Layout({ children, userEmail }: LayoutProps) {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col">
        <Header userEmail={userEmail} />
        <main className="flex-1 p-6 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}