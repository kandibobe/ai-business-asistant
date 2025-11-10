import apiClient from '../client'
import type { UserSettings } from '@/types'

export interface UpdateSettingsRequest {
  language?: string
  ai_role?: string
  response_style?: string
  ai_mode?: string
  notifications_enabled?: boolean
}

export const settingsApi = {
  /**
   * Get current user settings
   */
  async get(): Promise<UserSettings> {
    const response = await apiClient.get<UserSettings>('/settings/')
    return response.data
  },

  /**
   * Update user settings
   */
  async update(settings: UpdateSettingsRequest): Promise<UserSettings> {
    const response = await apiClient.put<UserSettings>('/settings/', settings)
    return response.data
  },
}

export default settingsApi
