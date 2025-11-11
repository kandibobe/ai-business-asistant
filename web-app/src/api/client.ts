import axios, { AxiosInstance, AxiosError } from 'axios'
import { store } from '@/store'
import { logout, setTokens } from '@/store/slices/authSlice'
import { showSnackbar } from '@/store/slices/uiSlice'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors and token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any

    // Handle 401 errors - token expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) {
          store.dispatch(logout())
          return Promise.reject(error)
        }

        // Attempt to refresh token
        const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {
          refresh_token: refreshToken,
        })

        const { access_token, refresh_token, token_type = 'Bearer' } = response.data
        store.dispatch(setTokens({ access_token, refresh_token, token_type }))

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        store.dispatch(logout())
        store.dispatch(
          showSnackbar({
            message: 'Session expired. Please login again.',
            severity: 'error',
          })
        )
        return Promise.reject(refreshError)
      }
    }

    // Handle other errors
    const errorMessage =
      (error.response?.data as any)?.detail ||
      error.message ||
      'An unexpected error occurred'

    store.dispatch(
      showSnackbar({
        message: errorMessage,
        severity: 'error',
      })
    )

    return Promise.reject(error)
  }
)

export default apiClient
