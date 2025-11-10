import { useCallback } from 'react'
import { useSnackbar } from 'notistack'

export interface ErrorContext {
  component?: string
  action?: string
  metadata?: Record<string, any>
}

export interface HandledError {
  message: string
  code?: string
  status?: number
  details?: any
}

export function useErrorHandler() {
  const { enqueueSnackbar } = useSnackbar()

  const handleError = useCallback(
    (error: unknown, context?: ErrorContext) => {
      // Log to console with context
      console.error('[Error Handler]', {
        error,
        context,
        timestamp: new Date().toISOString(),
      })

      // Parse error
      const parsedError = parseError(error)

      // Display user-friendly message
      const userMessage = getUserFriendlyMessage(parsedError, context)

      enqueueSnackbar(userMessage, {
        variant: getErrorVariant(parsedError.status),
        autoHideDuration: 5000,
        anchorOrigin: {
          vertical: 'top',
          horizontal: 'right',
        },
      })

      // Return parsed error for additional handling
      return parsedError
    },
    [enqueueSnackbar]
  )

  return { handleError }
}

function parseError(error: unknown): HandledError {
  // Axios error
  if (isAxiosError(error)) {
    return {
      message: error.response?.data?.detail || error.message || 'An error occurred',
      code: error.code,
      status: error.response?.status,
      details: error.response?.data,
    }
  }

  // Standard Error
  if (error instanceof Error) {
    return {
      message: error.message,
      details: error.stack,
    }
  }

  // String error
  if (typeof error === 'string') {
    return {
      message: error,
    }
  }

  // Unknown error
  return {
    message: 'An unexpected error occurred',
    details: error,
  }
}

function isAxiosError(error: any): error is {
  response?: { status?: number; data?: any };
  code?: string;
  message?: string;
} {
  return error?.isAxiosError === true || error?.response !== undefined
}

function getUserFriendlyMessage(error: HandledError, context?: ErrorContext): string {
  const { status, message, code } = error

  // Network errors
  if (code === 'ECONNABORTED' || code === 'ERR_NETWORK') {
    return 'Network connection failed. Please check your internet connection and try again.'
  }

  // HTTP status errors
  switch (status) {
    case 400:
      return message || 'Invalid request. Please check your input and try again.'
    case 401:
      return 'Your session has expired. Please log in again.'
    case 403:
      return 'You don\'t have permission to perform this action.'
    case 404:
      return `${context?.action || 'Resource'} not found.`
    case 409:
      return message || 'This item already exists.'
    case 422:
      return message || 'Validation error. Please check your input.'
    case 429:
      return 'Too many requests. Please wait a moment and try again.'
    case 500:
      return 'Server error. Our team has been notified and is working on it.'
    case 502:
    case 503:
    case 504:
      return 'Service temporarily unavailable. Please try again in a few moments.'
    default:
      return message || 'Something went wrong. Please try again.'
  }
}

function getErrorVariant(status?: number): 'default' | 'error' | 'warning' | 'info' {
  if (!status) return 'error'

  if (status >= 500) return 'error'
  if (status >= 400) return 'warning'
  return 'info'
}

// Export types
export type { ErrorContext as ErrorHandlerContext }
