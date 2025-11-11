import { Component, ErrorInfo, ReactNode } from 'react'
import { Box, Typography, Button, Paper, Collapse, Alert } from '@mui/material'
import { Error as ErrorIcon, Refresh, ExpandMore, BugReport } from '@mui/icons-material'
import { errorLogger } from '@/utils/errorLogger'

interface Props {
  children: ReactNode
  fallback?: ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
  showDetails: boolean
}

/**
 * Enhanced Error Boundary Component
 * Catches JavaScript errors anywhere in the child component tree
 * Features:
 * - Automatic error logging
 * - User-friendly error UI
 * - Error details for debugging (dev mode)
 * - Recovery options
 */
class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      showDetails: false,
    }
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return {
      hasError: true,
      error,
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to error logger
    errorLogger.logError(error, {
      component: 'ErrorBoundary',
      action: 'component_error',
      metadata: {
        componentStack: errorInfo.componentStack,
      },
    })

    this.props.onError?.(error, errorInfo)

    this.setState({
      error,
      errorInfo,
    })
  }

  handleReload = () => {
    window.location.reload()
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
      showDetails: false,
    })
  }

  toggleDetails = () => {
    this.setState(prev => ({ showDetails: !prev.showDetails }))
  }

  handleReportBug = () => {
    const report = {
      error: this.state.error?.toString(),
      stack: this.state.error?.stack,
      componentStack: this.state.errorInfo?.componentStack,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
      url: window.location.href,
    }

    navigator.clipboard.writeText(JSON.stringify(report, null, 2))
      .then(() => alert('Error report copied to clipboard'))
      .catch(() => alert('Failed to copy error report'))
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      const isDev = import.meta.env.DEV

      return (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            p: 3,
            backgroundColor: 'background.default',
          }}
        >
          <Paper
            sx={{
              maxWidth: 700,
              p: 4,
              textAlign: 'center',
              borderRadius: 3,
              boxShadow: 3,
            }}
          >
            <ErrorIcon
              sx={{
                fontSize: 100,
                color: 'error.main',
                mb: 2,
                opacity: 0.9,
              }}
            />

            <Typography variant="h4" fontWeight={700} gutterBottom>
              Oops! Something went wrong
            </Typography>

            <Typography variant="body1" color="text.secondary" sx={{ mb: 3, lineHeight: 1.7 }}>
              We're sorry for the inconvenience. An unexpected error has occurred.
              {isDev ? ' Check the details below or try reloading the page.' : ' Please try reloading the page.'}
            </Typography>

            {isDev && this.state.error && (
              <Box sx={{ mb: 3 }}>
                <Button
                  size="small"
                  onClick={this.toggleDetails}
                  endIcon={
                    <ExpandMore
                      sx={{
                        transform: this.state.showDetails ? 'rotate(180deg)' : 'rotate(0)',
                        transition: 'transform 0.3s',
                      }}
                    />
                  }
                >
                  {this.state.showDetails ? 'Hide' : 'Show'} Error Details
                </Button>

                <Collapse in={this.state.showDetails}>
                  <Alert severity="error" sx={{ mt: 2, textAlign: 'left' }}>
                    <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Error Message:
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 2, fontFamily: 'monospace' }}>
                        {this.state.error.toString()}
                      </Typography>

                      {this.state.error.stack && (
                        <>
                          <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                            Stack Trace:
                          </Typography>
                          <Typography
                            variant="caption"
                            component="pre"
                            sx={{
                              fontSize: 11,
                              fontFamily: 'monospace',
                              whiteSpace: 'pre-wrap',
                              wordBreak: 'break-word',
                            }}
                          >
                            {this.state.error.stack}
                          </Typography>
                        </>
                      )}

                      {this.state.errorInfo?.componentStack && (
                        <>
                          <Typography variant="subtitle2" fontWeight={600} gutterBottom sx={{ mt: 2 }}>
                            Component Stack:
                          </Typography>
                          <Typography
                            variant="caption"
                            component="pre"
                            sx={{
                              fontSize: 11,
                              fontFamily: 'monospace',
                              whiteSpace: 'pre-wrap',
                              wordBreak: 'break-word',
                            }}
                          >
                            {this.state.errorInfo.componentStack}
                          </Typography>
                        </>
                      )}
                    </Box>
                  </Alert>
                </Collapse>
              </Box>
            )}

            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Button
                variant="outlined"
                startIcon={<Refresh />}
                onClick={this.handleReset}
                size="large"
              >
                Try Again
              </Button>

              <Button
                variant="contained"
                onClick={this.handleReload}
                size="large"
              >
                Reload Page
              </Button>

              {isDev && (
                <Button
                  variant="outlined"
                  color="info"
                  startIcon={<BugReport />}
                  onClick={this.handleReportBug}
                  size="large"
                >
                  Copy Report
                </Button>
              )}
            </Box>

            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ mt: 3, display: 'block' }}
            >
              If this problem persists, please contact support with the error report.
            </Typography>
          </Paper>
        </Box>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
