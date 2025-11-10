import { useState, useCallback } from 'react'

export interface RetryOptions {
  maxAttempts?: number
  delay?: number
  backoff?: 'linear' | 'exponential'
  onRetry?: (attempt: number) => void
}

export interface RetryState {
  isRetrying: boolean
  attempt: number
  error: Error | null
}

export function useRetry<T>(
  operation: () => Promise<T>,
  options: RetryOptions = {}
) {
  const {
    maxAttempts = 3,
    delay = 1000,
    backoff = 'exponential',
    onRetry,
  } = options

  const [state, setState] = useState<RetryState>({
    isRetrying: false,
    attempt: 0,
    error: null,
  })

  const execute = useCallback(async (): Promise<T> => {
    setState({ isRetrying: true, attempt: 0, error: null })

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        const result = await operation()
        setState({ isRetrying: false, attempt, error: null })
        return result
      } catch (error) {
        const isLastAttempt = attempt === maxAttempts

        if (isLastAttempt) {
          setState({
            isRetrying: false,
            attempt,
            error: error instanceof Error ? error : new Error(String(error)),
          })
          throw error
        }

        // Calculate delay based on backoff strategy
        const currentDelay = backoff === 'exponential'
          ? delay * Math.pow(2, attempt - 1)
          : delay * attempt

        // Notify about retry
        onRetry?.(attempt)

        setState({
          isRetrying: true,
          attempt,
          error: error instanceof Error ? error : new Error(String(error)),
        })

        // Wait before next attempt
        await sleep(currentDelay)
      }
    }

    throw new Error('Max retry attempts reached')
  }, [operation, maxAttempts, delay, backoff, onRetry])

  const reset = useCallback(() => {
    setState({ isRetrying: false, attempt: 0, error: null })
  }, [])

  return {
    execute,
    reset,
    ...state,
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}
