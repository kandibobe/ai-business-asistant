import apiClient from '../client'
import type { Document } from '@/types'

export interface DocumentListResponse {
  documents: Document[]
  total: number
  active_document_id: number | null
}

export interface DocumentContentResponse {
  id: number
  file_name: string
  content: string
  summary: string | null
  keywords: string | null
}

export const documentsApi = {
  /**
   * Get all documents for the current user
   */
  async list(): Promise<DocumentListResponse> {
    const response = await apiClient.get<DocumentListResponse>('/documents/')
    return response.data
  },

  /**
   * Upload a new document
   */
  async upload(
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<Document> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post<Document>('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(percentCompleted)
        }
      },
    })

    return response.data
  },

  /**
   * Get document by ID with full content
   */
  async getById(documentId: number): Promise<DocumentContentResponse> {
    const response = await apiClient.get<DocumentContentResponse>(
      `/documents/${documentId}`
    )
    return response.data
  },

  /**
   * Delete a document
   */
  async delete(documentId: number): Promise<void> {
    await apiClient.delete(`/documents/${documentId}`)
  },

  /**
   * Set document as active for chat
   */
  async activate(documentId: number): Promise<void> {
    await apiClient.put(`/documents/${documentId}/activate`)
  },
}

export default documentsApi
