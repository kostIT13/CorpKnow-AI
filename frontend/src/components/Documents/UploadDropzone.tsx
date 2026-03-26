// src/components/Documents/UploadDropzone.tsx
import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useDocuments } from '../../hooks';


interface UploadDropzoneProps {
  onUploadSuccess?: () => void;
}

export default function UploadDropzone({ onUploadSuccess }: UploadDropzoneProps) {
  const { uploadDocument, uploading } = useDocuments();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    try {
      await uploadDocument(file);
      onUploadSuccess?.();
    } catch (error) {
      // Ошибка уже обработана в useDocuments
    }
  }, [uploadDocument, onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
    disabled: uploading,
  });

  return (
    <div
      {...getRootProps()}
      className={`
        border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all
        ${isDragActive 
          ? 'border-blue-500 bg-blue-50 scale-[1.02]' 
          : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
        }
        ${uploading ? 'opacity-60 cursor-not-allowed' : ''}
      `}
    >
      <input {...getInputProps()} />
      
      {uploading ? (
        <div className="flex flex-col items-center gap-3">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
          <p className="text-gray-600 font-medium">Обработка документа...</p>
          <p className="text-sm text-gray-400">Создаём эмбеддинги для поиска</p>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-3">
          {/* Иконка загрузки */}
          <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center">
            <svg className="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          
          <div>
            <p className="text-gray-700 font-medium">
              {isDragActive ? 'Отпустите файл здесь' : 'Перетащите файл или нажмите для выбора'}
            </p>
            <p className="text-sm text-gray-400 mt-1">PDF, TXT, DOCX до 10 МБ</p>
          </div>
        </div>
      )}
    </div>
  );
}