# 🤖 CorpKnow AI
**Умный корпоративный ассистент знаний с технологией RAG (Retrieval-Augmented Generation)** 

Загружайте документы и получайте точные ответы на вопросы на основе их содержания.

## ✨ Возможности

* 📤 Загрузка документов — Поддержка PDF, TXT, DOCX файлов до 10 МБ
* 🔍 Умный поиск — Векторный поиск по всем документам пользователя через ChromaDB
* 💬 Чат с контекстом — Диалог с историей сообщений и источниками ответов
* 👤 Авторизация — Регистрация, вход, защита маршрутов через JWT
* 🗂️ Управление документами — Просмотр статуса обработки, удаление, статистика чанков
* 🔄 Асинхронная обработка — Фоновая индексация документов без блокировки UI
* 🎨 Адаптивный UI — Современный интерфейс на React + Tailwind CSS

## 🛠 Технологический стек

**Frontend:**
* React 18 + TypeScript
* Vite (сборка и dev-сервер)
* Tailwind CSS + Headless UI
* React Router DOM (навигация)
* Axios (HTTP-клиент)
* React Hot Toast (уведомления)
* React Dropzone (загрузка файлов)

**Backend:**
* Python 3.12 + FastAPI
* SQLAlchemy + Alembic (ORM + миграции)
* PostgreSQL (основная БД)
* ChromaDB (векторное хранилище)
* Pydantic (валидация данных)
* Uvicorn (ASGI-сервер)

**AI / ML:**
* Ollama (локальные LLM)
* Модель: llama3.2:3b (генерация ответов)
* Эмбеддинги: nomic-embed-text

**Инфраструктура:**
* Docker + Docker Compose
* Nginx (раздача статики в продакшене)


## 🚀 Быстрый старт

**Требования**
* Docker 24.0+
* Docker Compose 2.20+
* Ollama 0.1.30+ (локально)
* ОЗУ 8 ГБ (рекомендуется 16 ГБ для LLM)

### Шаг 1: Клонируйте репозиторий
```bash
git clone https://github.com/kostIT13/CorpKnow-AI.git
cd CorpKnow-AI
```

### Шаг 2: Настройте окружение
```bash
cp .env.example .env
```

### Шаг 3: Запустите Ollama (локально)
```bash
# Скачайте необходимые модели
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# Запустите Ollama
OLLAMA_HOST=0.0.0.0 ollama serve
```

### Шаг 4: Запустите проект
```bash
# Сборка и запуск всех сервисов
docker compose up --build

# Или в фоновом режиме
docker compose up -d --build

# Просмотр логов
docker compose logs -f
```

### Шаг 5: Откройте приложение
* Frontend: http://localhost:5173
* Backend API: http://localhost:8000
* API Docs (Swagger): http://localhost:8000/docs

## 📁 Структура проекта
```
CorpKnow-AI/
├── backend/
│   ├── src/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Конфигурация, безопасность
│   │   ├── models/           # SQLAlchemy модели
│   │   ├── services/         # Бизнес-логика
│   │   │   ├── rag/          # RAG-сервис
│   │   │   ├── chat/         # Управление чатами
│   │   │   └── document/     # Обработка документов
│   │   └── main.py           # Точка входа FastAPI
│   ├── alembic/              # Миграции БД
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── api/              # API-клиенты
│   │   ├── components/       # UI-компоненты
│   │   ├── hooks/            # Кастомные хуки
│   │   ├── pages/            # Страницы
│   │   ├── types/            # TypeScript типы
│   │   ├── App.tsx           # Роутинг
│   │   └── main.tsx          # Точка входа React
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── nginx.conf
│
├── uploads/                  # Загруженные файлы
├── docker-compose.yml
├── .env.example
└── README.md
```
