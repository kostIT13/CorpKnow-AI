interface SourceCardProps {
  filename: string;
  onClick?: () => void;
}

export default function SourceCard({ filename, onClick }: SourceCardProps) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded-lg hover:border-blue-400 hover:shadow-sm transition text-left"
    >
      <div className="w-8 h-8 bg-gray-100 rounded flex items-center justify-center shrink-0">
        <span className="text-sm">
          {filename.endsWith('.pdf') ? '📄' : 
           filename.endsWith('.docx') ? '📘' : '📝'}
        </span>
      </div>
      
      <div className="min-w-0">
        <p className="text-sm font-medium text-gray-700 truncate max-w-37.5">
          {filename}
        </p>
        <p className="text-xs text-gray-400">Источник</p>
      </div>
    </button>
  );
}