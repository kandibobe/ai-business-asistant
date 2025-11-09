import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import type { ChatMessage } from '@/types'

interface ChatState {
  messages: ChatMessage[]
  isLoading: boolean
  error: string | null
}

const initialState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
}

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action: PayloadAction<ChatMessage>) => {
      state.messages.push(action.payload)
    },
    sendMessageStart: (state) => {
      state.isLoading = true
      state.error = null
    },
    sendMessageSuccess: (state, action: PayloadAction<ChatMessage>) => {
      state.messages.push(action.payload)
      state.isLoading = false
    },
    sendMessageFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false
      state.error = action.payload
    },
    clearMessages: (state) => {
      state.messages = []
    },
    loadHistory: (state, action: PayloadAction<ChatMessage[]>) => {
      state.messages = action.payload
    },
  },
})

export const {
  addMessage,
  sendMessageStart,
  sendMessageSuccess,
  sendMessageFailure,
  clearMessages,
  loadHistory,
} = chatSlice.actions

export default chatSlice.reducer
