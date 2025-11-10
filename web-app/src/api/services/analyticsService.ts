/**
 * Analytics API service
 */
import apiClient from '../client'

export interface UserStats {
  total_documents: number
  total_questions: number
  average_response_time: number
  documents_by_type: Record<string, number>
  active_document?: {
    id: number
    file_name: string
    document_type: string
  }
  user_since?: string
}

export interface DashboardStats {
  documents_today: number
  questions_today: number
  total_documents: number
  total_questions: number
  activity_chart: Array<{
    date: string
    questions: number
  }>
  recent_documents: Array<{
    id: number
    file_name: string
    document_type: string
    uploaded_at?: string
    is_active: boolean
  }>
  is_premium: boolean
}

export interface DocumentStats {
  document: {
    id: number
    file_name: string
    document_type: string
    file_size: number
    uploaded_at?: string
    processed_at?: string
    status: string
  }
  total_questions: number
  average_response_time: number
  recent_questions: Array<{
    question: string
    answer: string
    created_at?: string
    response_time?: number
  }>
}

export const analyticsService = {
  /**
   * Get user statistics
   */
  getUserStats: async (): Promise<UserStats> => {
    const response = await apiClient.get('/analytics/stats')
    return response.data
  },

  /**
   * Get dashboard statistics
   */
  getDashboardStats: async (): Promise<DashboardStats> => {
    const response = await apiClient.get('/analytics/dashboard')
    return response.data
  },

  /**
   * Get statistics for a specific document
   */
  getDocumentStats: async (documentId: number): Promise<DocumentStats> => {
    const response = await apiClient.get(`/analytics/documents/${documentId}/stats`)
    return response.data
  }
}
