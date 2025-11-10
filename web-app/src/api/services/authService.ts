/**
 * Authentication API service
 */
import apiClient from '../client'

export interface RegisterRequest {
  username: string
  password: string
  email?: string
  first_name?: string
  last_name?: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface User {
  id: number
  user_id: number
  username: string
  first_name?: string
  last_name?: string
  language: string
  is_premium: boolean
  created_at?: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface AuthResponse {
  user: User
  tokens: TokenResponse
}

export const authService = {
  /**
   * Register a new user
   */
  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/register', data)
    return response.data
  },

  /**
   * Login user
   */
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login', data)
    return response.data
  },

  /**
   * Get current user info
   */
  me: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me')
    return response.data
  },

  /**
   * Refresh access token
   */
  refresh: async (): Promise<TokenResponse> => {
    const response = await apiClient.post('/auth/refresh')
    return response.data
  }
}
