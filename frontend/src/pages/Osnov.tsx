import { useNavigate } from 'react-router-dom';

export default function Osnov() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b bg-white">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">CorpKnow AI</h1>
          <div className="space-x-4">
            <button onClick={() => navigate('/login')} className="text-gray-700 hover:text-gray-900">
              Войти
            </button>
            <button onClick={() => navigate('/register')} className="px-4 py-2 bg-blue-600 text-white rounded-lg">
              Регистрация
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h2 className="text-4xl font-bold mb-4">Умный поиск по документам</h2>
        <p className="text-xl text-gray-600 mb-8">Загружай документы и задавай вопросы AI</p>
        <button
          onClick={() => navigate('/register')}
          className="px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold"
        >
          Начать бесплатно
        </button>
      </main>
    </div>
  );
}