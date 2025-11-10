/**
 * Documents API service
 */
import apiClient from '../client'

export interface Document {
  id: number
  file_name: string
  document_type: string
  file_size: number
  status: string
  is_active: boolean
  uploaded_at?: string
  processed_at?: string
  summary?: string
  page_count?: number
  word_count?: number
}

export interface DocumentListResponse {
  documents: Document[]
  total: number
  page: number
  page_size: number
}

export interface UploadResponse {
  id: number
  file_name: string
  document_type: string
  file_size: number
  status: string
  message: string
}

export const documentService = {
  /**
   * Get list of user's documents
   */
  list: async (page: number = 1, page_size: number = 20): Promise<DocumentListResponse> => {
    const response = await apiClient.get('/documents', {
      params: { page, page_size }
    })
    return response.data
  },

  /**
   * Upload a new document
   */
  upload: async (
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<UploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = (progressEvent.loaded / progressEvent.total) * 100
          onProgress(progress)
        }
      }
    })
    return response.data
  },

  /**
   * Get details of a specific document
   */
  get: async (documentId: number): Promise<Document> => {
    const response = await apiClient.get(`/documents/${documentId}`)
    return response.data
  },

  /**
   * Delete a document
   */
  delete: async (documentId: number): Promise<void> => {
    await apiClient.delete(`/documents/${documentId}`)
  },

  /**
   * Activate a document (set as active for chat context)
   */
  activate: async (documentId: number): Promise<void> => {
    await apiClient.put(`/documents/${documentId}/activate`)
  }
}
