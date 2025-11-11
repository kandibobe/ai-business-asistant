import { useState, useCallback } from 'react'

export interface LoadingState {
  isLoading: boolean
  error: Error | null
  data: any | null
}

export interface UseLoadingOptions {
  initialLoading?: boolean
  onSuccess?: (data: any) => void
  onError?: (error: Error) => void
}

export function useLoading<T = any>(options: UseLoadingOptions = {}) {
  const { initialLoading = false, onSuccess, onError } = options

  const [state, setState] = useState<LoadingState>({
    isLoading: initialLoading,
    error: null,
    data: null,
  })

  const startLoading = useCallback(() => {
    setState({
      isLoading: true,
      error: null,
      data: null,
    })
  }, [])

  const stopLoading = useCallback((data?: any) => {
    setState({
      isLoading: false,
      error: null,
      data: data ?? null,
    })
    if (data && onSuccess) {
      onSuccess(data)
    }
  }, [onSuccess])

  const setError = useCallback((error: Error) => {
    setState({
      isLoading: false,
      error,
      data: null,
    })
    if (onError) {
      onError(error)
    }
  }, [onError])

  const execute = useCallback(async <R = T>(
    asyncFunction: () => Promise<R>
  ): Promise<R | undefined> => {
    startLoading()
    try {
      const result = await asyncFunction()
      stopLoading(result)
      return result
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err))
      setError(error)
      return undefined
    }
  }, [startLoading, stopLoading, setError])

  const reset = useCallback(() => {
    setState({
      isLoading: false,
      error: null,
      data: null,
    })
  }, [])

  return {
    ...state,
    startLoading,
    stopLoading,
    setError,
    execute,
    reset,
  }
}

// Hook for multiple parallel operations
export function useMultipleLoading(count: number) {
  const [loadingStates, setLoadingStates] = useState<boolean[]>(
    Array(count).fill(false)
  )

  const setLoading = useCallback((index: number, isLoading: boolean) => {
    setLoadingStates(prev => {
      const newStates = [...prev]
      newStates[index] = isLoading
      return newStates
    })
  }, [])

  const isAnyLoading = loadingStates.some(state => state)
  const isAllLoading = loadingStates.every(state => state)

  return {
    loadingStates,
    setLoading,
    isAnyLoading,
    isAllLoading,
  }
}
