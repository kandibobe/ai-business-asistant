/**
 * Error Logger Utility
 * Centralized error logging with context and metadata
 */

export interface ErrorLog {
  message: string
  level: 'error' | 'warn' | 'info'
  timestamp: string
  userAgent?: string
  url?: string
  component?: string
  action?: string
  metadata?: Record<string, any>
  stack?: string
}

class ErrorLogger {
  private logs: ErrorLog[] = []
  private maxLogs = 100
  private isDevelopment = import.meta.env.DEV

  /**
   * Log an error with context
   */
  logError(error: Error | string, context?: {
    component?: string
    action?: string
    metadata?: Record<string, any>
  }): void {
    const log: ErrorLog = {
      message: error instanceof Error ? error.message : error,
      level: 'error',
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href,
      component: context?.component,
      action: context?.action,
      metadata: context?.metadata,
      stack: error instanceof Error ? error.stack : undefined,
    }

    this.addLog(log)

    // Console log in development
    if (this.isDevelopment) {
      console.error('[Error]', log)
    }

    // Send to error tracking service (Sentry, LogRocket, etc.)
    this.sendToErrorService(log)
  }

  /**
   * Log a warning
   */
  logWarning(message: string, context?: Record<string, any>): void {
    const log: ErrorLog = {
      message,
      level: 'warn',
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href,
      metadata: context,
    }

    this.addLog(log)

    if (this.isDevelopment) {
      console.warn('[Warning]', log)
    }
  }

  /**
   * Log info
   */
  logInfo(message: string, context?: Record<string, any>): void {
    const log: ErrorLog = {
      message,
      level: 'info',
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href,
      metadata: context,
    }

    this.addLog(log)

    if (this.isDevelopment) {
      console.info('[Info]', log)
    }
  }

  /**
   * Get all logs
   */
  getLogs(): ErrorLog[] {
    return [...this.logs]
  }

  /**
   * Get logs by level
   */
  getLogsByLevel(level: 'error' | 'warn' | 'info'): ErrorLog[] {
    return this.logs.filter(log => log.level === level)
  }

  /**
   * Clear all logs
   */
  clearLogs(): void {
    this.logs = []
  }

  /**
   * Export logs as JSON
   */
  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2)
  }

  /**
   * Add log to history
   */
  private addLog(log: ErrorLog): void {
    this.logs.unshift(log)

    // Keep only last N logs
    if (this.logs.length > this.maxLogs) {
      this.logs = this.logs.slice(0, this.maxLogs)
    }

    // Store in localStorage for persistence
    try {
      localStorage.setItem('error_logs', JSON.stringify(this.logs.slice(0, 50)))
    } catch (e) {
      // Ignore localStorage errors
    }
  }

  /**
   * Send error to remote error tracking service
   */
  private sendToErrorService(log: ErrorLog): void {
    // TODO: Integrate with Sentry, LogRocket, or custom error tracking service
    // Example:
    // if (window.Sentry) {
    //   window.Sentry.captureException(new Error(log.message), {
    //     tags: {
    //       component: log.component,
    //       action: log.action,
    //     },
    //     extra: log.metadata,
    //   })
    // }

    // For now, just track in console
    if (!this.isDevelopment && import.meta.env.VITE_API_URL) {
      // Send to backend logging endpoint
      fetch(`${import.meta.env.VITE_API_URL}/api/logs/error`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(log),
      }).catch(() => {
        // Silently fail if logging endpoint is not available
      })
    }
  }

  /**
   * Initialize logger (load persisted logs)
   */
  initialize(): void {
    try {
      const stored = localStorage.getItem('error_logs')
      if (stored) {
        this.logs = JSON.parse(stored)
      }
    } catch (e) {
      // Ignore initialization errors
    }
  }
}

// Export singleton instance
export const errorLogger = new ErrorLogger()

// Initialize on import
errorLogger.initialize()

// Global error handler
window.addEventListener('error', (event) => {
  errorLogger.logError(event.error || event.message, {
    component: 'Global',
    action: 'unhandled_error',
    metadata: {
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
    },
  })
})

// Global unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
  errorLogger.logError(
    event.reason instanceof Error
      ? event.reason
      : String(event.reason),
    {
      component: 'Global',
      action: 'unhandled_promise_rejection',
    }
  )
})
