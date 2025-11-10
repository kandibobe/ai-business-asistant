import apiClient from '../client'

export interface UserStatsResponse {
  total_documents: number
  total_questions: number
  avg_response_time_ms: number | null
  total_sessions: number
  documents_by_type: Record<string, number>
  recent_activity: any[]
}

export interface DocumentStatsResponse {
  document_id: number
  total_questions: number
  avg_response_time_ms: number | null
  question_history: any[]
}

export const analyticsApi = {
  /**
   * Get user statistics
   */
  async getUserStats(): Promise<UserStatsResponse> {
    const response = await apiClient.get<UserStatsResponse>('/analytics/stats')
    return response.data
  },

  /**
   * Get statistics for a specific document
   */
  async getDocumentStats(documentId: number): Promise<DocumentStatsResponse> {
    const response = await apiClient.get<DocumentStatsResponse>(
      `/analytics/documents/${documentId}`
    )
    return response.data
  },
}

export default analyticsApi
