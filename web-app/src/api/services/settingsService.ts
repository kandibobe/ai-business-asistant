/**
 * Settings API service
 */
import apiClient from '../client'

export interface Settings {
  language: string
  ai_role?: string
  ai_style?: string
  mode?: string
  notifications_enabled: boolean
}

export interface SettingsUpdateRequest {
  language?: string
  ai_role?: string
  ai_style?: string
  mode?: string
  notifications_enabled?: boolean
}

export interface SettingsUpdateResponse {
  success: boolean
  message: string
  settings: Settings
}

export const settingsService = {
  /**
   * Get current user settings
   */
  get: async (): Promise<Settings> => {
    const response = await apiClient.get('/settings')
    return response.data
  },

  /**
   * Update user settings
   */
  update: async (data: SettingsUpdateRequest): Promise<SettingsUpdateResponse> => {
    const response = await apiClient.put('/settings', data)
    return response.data
  },

  /**
   * Quick change language
   */
  changeLanguage: async (language: string): Promise<void> => {
    await apiClient.post('/settings/language', null, {
      params: { language }
    })
  }
}
