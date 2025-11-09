import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import type { UserSettings } from '@/types'

interface SettingsState extends UserSettings {
  isLoading: boolean
  isSaving: boolean
  error: string | null
}

const initialState: SettingsState = {
  language: 'en',
  ai_role: 'assistant',
  response_style: 'standard',
  ai_mode: 'standard',
  notifications_enabled: true,
  theme: 'light',
  isLoading: false,
  isSaving: false,
  error: null,
}

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    loadSettingsStart: (state) => {
      state.isLoading = true
    },
    loadSettingsSuccess: (state, action: PayloadAction<UserSettings>) => {
      Object.assign(state, action.payload)
      state.isLoading = false
    },
    saveSettingsStart: (state) => {
      state.isSaving = true
      state.error = null
    },
    saveSettingsSuccess: (state, action: PayloadAction<Partial<UserSettings>>) => {
      Object.assign(state, action.payload)
      state.isSaving = false
    },
    saveSettingsFailure: (state, action: PayloadAction<string>) => {
      state.isSaving = false
      state.error = action.payload
    },
    updateLanguage: (state, action: PayloadAction<string>) => {
      state.language = action.payload
    },
    updateTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload
      localStorage.setItem('theme', action.payload)
    },
    toggleNotifications: (state) => {
      state.notifications_enabled = !state.notifications_enabled
    },
  },
})

export const {
  loadSettingsStart,
  loadSettingsSuccess,
  saveSettingsStart,
  saveSettingsSuccess,
  saveSettingsFailure,
  updateLanguage,
  updateTheme,
  toggleNotifications,
} = settingsSlice.actions

export default settingsSlice.reducer
