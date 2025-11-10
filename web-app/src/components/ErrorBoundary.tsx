import React, { Component, ErrorInfo, ReactNode } from 'react'
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  Alert,
} from '@mui/material'
import { ErrorOutline, Refresh } from '@mui/icons-material'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    }
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to console in development
    console.error('Error caught by ErrorBoundary:', error, errorInfo)

    // Update state with error details
    this.setState({
      error,
      errorInfo,
    })

    // TODO: Send error to monitoring service (e.g., Sentry)
    // if (process.env.VITE_SENTRY_DSN) {
    //   Sentry.captureException(error, { extra: errorInfo })
    // }
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    })
    // Reload the page to reset application state
    window.location.reload()
  }

  handleGoBack = () => {
    window.history.back()
  }

  render() {
    if (this.state.hasError) {
      // Custom fallback UI provided
      if (this.props.fallback) {
        return this.props.fallback
      }

      // Default error UI
      return (
        <Container maxWidth="md" sx={{ mt: 8 }}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
              }}
            >
              <ErrorOutline
                sx={{ fontSize: 80, color: 'error.main', mb: 2 }}
              />

              <Typography variant="h4" fontWeight={700} gutterBottom>
                Oops! Something went wrong
              </Typography>

              <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                We encountered an unexpected error. Don't worry, your data is safe.
              </Typography>

              {this.state.error && (
                <Alert severity="error" sx={{ mb: 3, width: '100%' }}>
                  <Typography variant="body2" fontWeight={600}>
                    Error: {this.state.error.toString()}
                  </Typography>
                  {process.env.NODE_ENV === 'development' && (
                    <Typography
                      variant="caption"
                      component="pre"
                      sx={{
                        mt: 1,
                        whiteSpace: 'pre-wrap',
                        fontSize: '0.7rem',
                      }}
                    >
                      {this.state.errorInfo?.componentStack}
                    </Typography>
                  )}
                </Alert>
              )}

              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  startIcon={<Refresh />}
                  onClick={this.handleReset}
                >
                  Reload Page
                </Button>
                <Button variant="outlined" onClick={this.handleGoBack}>
                  Go Back
                </Button>
              </Box>

              <Typography
                variant="caption"
                color="text.secondary"
                sx={{ mt: 3 }}
              >
                If this problem persists, please contact support
              </Typography>
            </Box>
          </Paper>
        </Container>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
