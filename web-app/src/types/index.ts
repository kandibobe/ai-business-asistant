// User types
export interface User {
  id: number
  user_id: number
  username: string | null
  first_name: string | null
  last_name: string | null
  email?: string
  language: string
  ai_role: string
  response_style: string
  ai_mode: string
  created_at: string
  is_premium: boolean
  premium_expires_at?: string
  role?: string
}

// Document types
export interface Document {
  id: number
  file_name: string
  file_path: string | null
  content: string | null
  document_type: 'pdf' | 'excel' | 'word' | 'url' | 'audio'
  source_url: string | null
  file_size: number | null
  word_count: number | null
  char_count: number | null
  language_detected: string | null
  summary: string | null
  keywords: string | null
  uploaded_at: string
  processed_at: string | null
  is_active: boolean
  status?: string
}

// Chat message types
export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  document_id?: number
  response_time?: number
}

// Statistics types
export interface UserStats {
  total_docs: number
  active_doc: string
  docs_this_month: number
  questions_asked: number
  avg_response_time: string
  accuracy: number
  pdf_count: number
  excel_count: number
  word_count: number
  url_count: number
  audio_count: number
  first_visit: string
  last_activity: string
  streak_days: number
  is_premium: boolean
  total_words: number
  total_chars: number
  total_size_mb: number
}

// API Response types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

// Auth types
export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
}

// Settings types
export interface UserSettings {
  language: string
  ai_role: string
  response_style: string
  ai_mode: string
  notifications_enabled: boolean
  theme: 'light' | 'dark'
}

// Premium types
export interface PremiumPlan {
  id: string
  name: string
  price_monthly: number
  price_yearly: number
  features: string[]
  limits: {
    max_documents: number
    max_file_size: number
    api_calls_per_day: number
  }
}

// Developer Tool types
export interface ToolRequest {
  tool: string
  input: string | Record<string, any>
  options?: Record<string, any>
}

export interface ToolResponse {
  success: boolean
  result: string | Record<string, any>
  execution_time?: number
}
