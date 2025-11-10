import apiClient from '../client'
import type { ChatMessage } from '@/types'

export interface SendMessageRequest {
  message: string
  document_id?: number
}

export interface ChatResponse {
  message: string
  response_time_ms: number
  cached: boolean
  tokens_used: number | null
}

export interface ChatHistoryResponse {
  document_id: number
  messages: ChatMessage[]
  total_messages: number
}

export const chatApi = {
  /**
   * Send a message to AI
   */
  async sendMessage(
    message: string,
    documentId?: number
  ): Promise<ChatResponse> {
    const payload: SendMessageRequest = {
      message,
    }

    if (documentId !== undefined) {
      payload.document_id = documentId
    }

    const response = await apiClient.post<ChatResponse>('/chat/message', payload)
    return response.data
  },

  /**
   * Get chat history for a document
   */
  async getHistory(documentId: number): Promise<ChatHistoryResponse> {
    const response = await apiClient.get<ChatHistoryResponse>(
      `/chat/history/${documentId}`
    )
    return response.data
  },
}

export default chatApi
