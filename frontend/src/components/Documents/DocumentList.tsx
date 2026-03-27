import UploadDropzone from './UploadDropzone';
import DocumentItem from './DocumentItem';
import { useDocuments } from '../../hooks';

export default function DocumentList() {
  const { documents, loading } = useDocuments();

  const handleUploadSuccess = () => {
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">📁 Ваши документы</h2>
        <p className="text-sm text-gray-500 mt-1">
          Загрузите документы для поиска по ним
        </p>
      </div>

      <UploadDropzone onUploadSuccess={handleUploadSuccess} />

      {documents.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-gray-500">Нет загруженных документов</p>
          <p className="text-sm text-gray-400 mt-1">Загрузите первый файл выше</p>
        </div>
      ) : (
        <div className="space-y-3">
          {documents.map(doc => (
            <DocumentItem key={doc.id} doc={doc} />
          ))}
        </div>
      )}
    </div>
  );
}