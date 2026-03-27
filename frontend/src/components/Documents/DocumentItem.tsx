import { useDocuments } from '../../hooks';
import type { Document } from '../../types';

interface DocumentItemProps {
  doc: Document;
}

function getStatusBadge(status: Document['status']) {
  const styles = {
    pending: 'bg-yellow-100 text-yellow-800',
    processing: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };
  
  const labels = {
    pending: 'Ожидает',
    processing: 'Обрабатывается',
    completed: 'Готов',
    failed: 'Ошибка',
  };
  
  return (
    <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[status]}`}>
      {labels[status]}
    </span>
  );
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Б';
  const k = 1024;
  const sizes = ['Б', 'КБ', 'МБ', 'ГБ'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

export default function DocumentItem({ doc }: DocumentItemProps) {
  const { deleteDocument } = useDocuments();

  const handleDelete = async () => {
    await deleteDocument(doc.id);
  };

  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3 min-w-0">
          <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center shrink-0">
            <span className="text-lg">
              {doc.file_type.includes('pdf') ? '📄' : 
               doc.file_type.includes('word') ? '📘' : '📝'}
            </span>
          </div>
          
          <div className="min-w-0">
            <h4 className="font-medium text-gray-900 truncate">{doc.filename}</h4>
            <p className="text-sm text-gray-500">
              {formatFileSize(doc.file_size)} • {new Date(doc.created_at).toLocaleDateString('ru-RU')}
            </p>
            {doc.chunk_count > 0 && (
              <p className="text-xs text-gray-400 mt-0.5">
                {doc.chunk_count} чанков в индексе
              </p>
            )}
          </div>
        </div>
        
        <div className="flex items-center gap-2 shrink-0">
          {getStatusBadge(doc.status)}
          
          {doc.status === 'completed' && (
            <button
              onClick={handleDelete}
              className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded transition"
              title="Удалить"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          )}
        </div>
      </div>
      
      {doc.status === 'failed' && doc.error_message && (
        <p className="mt-2 text-sm text-red-600 bg-red-50 p-2 rounded">
          ⚠️ {doc.error_message}
        </p>
      )}
    </div>
  );
}