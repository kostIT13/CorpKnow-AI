// src/types/index.ts

// 🔹 Пользователь
export interface User {
  id: string;
  email: string;
  created_at: string;
}

// 🔹 Документ
export interface Document {
  id: string;
  filename: string;
  file_size: number;
  file_type: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  chunk_count: number;
  created_at: string;
  updated_at: string;
  error_message?: string;
}

// 🔹 Сообщение чата
export interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  created_at?: string;
}

// 🔹 Ответ от RAG
export interface ChatResponse {
  role: 'assistant';
  content: string;
  sources: string[];
  created_at: string;
}

// 🔹 Запрос к чату
export interface ChatRequest {
  query: string;
  chat_id?: string;
}

// 🔹 Токен авторизации
export interface AuthTokens {
  access_token: string;
  refresh_token?: string;
  token_type: string;
}

// 🔹 Данные для логина
export interface LoginRequest {
  email: string;
  password: string;
}

// 🔹 API Ответ с ошибкой
export interface ApiError {
  detail: string | { msg: string }[];
}