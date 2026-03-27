export interface User {
  id: string;
  email: string;
  created_at: string;
}

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

export interface Message {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  created_at?: string;
  is_starred?: boolean;
}

export interface ChatSession {
  chat_id: string;
  id?: string; 
  title: string;
  user_id?: string;
  created_at: string;
  updated_at: string;
  message_count?: number;
}

export interface ChatHistory {
  id: string;
  title: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  messages: Message[];
}

export interface ChatRequest {
  query: string;
  chat_id?: string;
}

export interface ChatResponse {
  role: 'assistant';
  content: string;
  sources: string[];
  chat_id: string;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token?: string;
  token_type: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface ApiError {
  detail: string | { msg: string }[];
}