/**
 * Chat API service
 */
import apiClient from '../client'

export interface SendMessageRequest {
  message: string
  document_id?: number
}

export interface MessageResponse {
  answer: string
  response_time: number
  timestamp: string
  question_id?: number
}

export interface ChatHistoryItem {
  id: number
  question: string
  answer: string
  timestamp: string
  response_time?: number
  document_id?: number
}

export interface ChatHistoryResponse {
  history: ChatHistoryItem[]
  total: number
}

export const chatService = {
  /**
   * Send a message to AI and get response
   */
  sendMessage: async (data: SendMessageRequest): Promise<MessageResponse> => {
    const response = await apiClient.post('/chat/message', data)
    return response.data
  },

  /**
   * Get chat history (optionally filtered by document)
   */
  getHistory: async (documentId?: number, limit: number = 50): Promise<ChatHistoryResponse> => {
    const params: any = { limit }
    if (documentId) {
      params.document_id = documentId
    }
    const response = await apiClient.get('/chat/history', { params })
    return response.data
  },

  /**
   * Clear chat history (optionally for specific document)
   */
  clearHistory: async (documentId?: number): Promise<void> => {
    const params: any = {}
    if (documentId) {
      params.document_id = documentId
    }
    await apiClient.delete('/chat/history', { params })
  }
}
