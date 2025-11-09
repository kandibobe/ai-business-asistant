import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import type { Document } from '@/types'

interface DocumentsState {
  documents: Document[]
  activeDocument: Document | null
  isLoading: boolean
  isUploading: boolean
  uploadProgress: number
  error: string | null
}

const initialState: DocumentsState = {
  documents: [],
  activeDocument: null,
  isLoading: false,
  isUploading: false,
  uploadProgress: 0,
  error: null,
}

const documentsSlice = createSlice({
  name: 'documents',
  initialState,
  reducers: {
    fetchDocumentsStart: (state) => {
      state.isLoading = true
      state.error = null
    },
    fetchDocumentsSuccess: (state, action: PayloadAction<Document[]>) => {
      state.documents = action.payload
      state.isLoading = false
    },
    fetchDocumentsFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false
      state.error = action.payload
    },
    uploadStart: (state) => {
      state.isUploading = true
      state.uploadProgress = 0
      state.error = null
    },
    uploadProgress: (state, action: PayloadAction<number>) => {
      state.uploadProgress = action.payload
    },
    uploadSuccess: (state, action: PayloadAction<Document>) => {
      state.documents.unshift(action.payload)
      state.activeDocument = action.payload
      state.isUploading = false
      state.uploadProgress = 100
    },
    uploadFailure: (state, action: PayloadAction<string>) => {
      state.isUploading = false
      state.error = action.payload
    },
    setActiveDocument: (state, action: PayloadAction<Document>) => {
      state.activeDocument = action.payload
    },
    deleteDocument: (state, action: PayloadAction<number>) => {
      state.documents = state.documents.filter(doc => doc.id !== action.payload)
      if (state.activeDocument?.id === action.payload) {
        state.activeDocument = null
      }
    },
    updateDocument: (state, action: PayloadAction<Document>) => {
      const index = state.documents.findIndex(doc => doc.id === action.payload.id)
      if (index !== -1) {
        state.documents[index] = action.payload
      }
      if (state.activeDocument?.id === action.payload.id) {
        state.activeDocument = action.payload
      }
    },
  },
})

export const {
  fetchDocumentsStart,
  fetchDocumentsSuccess,
  fetchDocumentsFailure,
  uploadStart,
  uploadProgress,
  uploadSuccess,
  uploadFailure,
  setActiveDocument,
  deleteDocument,
  updateDocument,
} = documentsSlice.actions

export default documentsSlice.reducer
