// src/pages/Documents.tsx
import { Layout } from '../components/Layout';

export default function Documents() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">📁 Документы</h2>
        <p className="text-gray-600">Здесь будет список загруженных файлов</p>
      </div>
    </Layout>
  );
}