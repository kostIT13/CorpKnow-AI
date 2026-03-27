# 🤖 CorpKnow AI
**Smart Corporate Knowledge Assistant with RAG Technology (Retrieval-Augmented Generation)** 

Upload documents and get precise answers to questions based on their content.

## ✨ Features

* 📤 Document Upload — Support for PDF, TXT, DOCX files up to 10 MB
* 🔍 Smart Search — Vector search across all user documents via ChromaDB
* 💬 Context-Aware Chat — Conversational interface with message history and answer sources
* 👤 Authentication — Registration, login, route protection via JWT
* 🗂️ Document Management — View processing status, delete files, chunk statistics
* 🔄 Async Processing — Background document indexing without blocking the UI
* 🎨 Responsive UI — Modern interface built with React + Tailwind CSS

## 🛠 Tech Stack

**Frontend:**
* React 18 + TypeScript
* Vite 
* Tailwind CSS + Headless UI
* React Router DOM 
* Axios 
* React Hot Toast 
* React Dropzone 

**Backend:**
* Python 3.12 + FastAPI
* SQLAlchemy + Alembic
* PostgreSQL 
* ChromaDB 
* Pydantic 
* Uvicorn 

**AI / ML:**
* Ollama (local LLMs)
* Model: llama3.2:3b (answer generation)
* Embeddings: nomic-embed-text

**Infrastructure:**
* Docker + Docker Compose
* Nginx (static file serving in production)


## 🚀 Quick Start

**Requirements**
* Docker 24.0+
* Docker Compose 2.20+
* Ollama 0.1.30+ (local)
* RAM: 8 GB minimum (16 GB recommended for LLM)

### Step 1: Clone the Repository
```bash
git clone https://github.com/kostIT13/CorpKnow-AI.git
cd CorpKnow-AI
```

### Step 2: Configure Environment
```bash
cp .env.example .env
```

### Step 3: Start Ollama (Local)
```bash

ollama pull llama3.2:3b
ollama pull nomic-embed-text

OLLAMA_HOST=0.0.0.0 ollama serve
```

### Step 4: Start the Project
```bash
docker compose up --build

docker compose up -d --build

docker compose logs -f
```

### Step 5: Open the Application
* Frontend: http://localhost:5173
* Backend API: http://localhost:8000
* API Docs (Swagger): http://localhost:8000/docs

## 📁 Project Structure
```
CorpKnow-AI/
├── backend/
│   ├── src/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Config, security, logging
│   │   ├── models/           # SQLAlchemy models
│   │   ├── services/         # Business logic
│   │   │   ├── rag/          # RAG service
│   │   │   ├── chat/         # Chat management
│   │   │   └── document/     # Document processing
│   │   └── main.py           # FastAPI entry point
│   ├── alembic/              # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── api/              # API clients
│   │   ├── components/       # UI components
│   │   ├── hooks/            # Custom hooks
│   │   ├── pages/            # Pages
│   │   ├── types/            # TypeScript types
│   │   ├── App.tsx           # Routing
│   │   └── main.tsx          # React entry point
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── nginx.conf
│
├── uploads/                  # Uploaded files (volume)
├── docker-compose.yml
├── .env.example
└── README.md
```
