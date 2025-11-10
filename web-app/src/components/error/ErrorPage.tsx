import { Box, Button, Container, Typography, Paper } from '@mui/material'
import {
  ErrorOutline,
  Home,
  Refresh,
  ArrowBack,
} from '@mui/icons-material'
import { useNavigate } from 'react-router-dom'

export interface ErrorPageProps {
  title?: string
  message?: string
  statusCode?: number
  showBackButton?: boolean
  showHomeButton?: boolean
  showRefreshButton?: boolean
  onRetry?: () => void
}

export default function ErrorPage({
  title = 'Oops! Something went wrong',
  message = 'We encountered an unexpected error. Please try again.',
  statusCode,
  showBackButton = true,
  showHomeButton = true,
  showRefreshButton = true,
  onRetry,
}: ErrorPageProps) {
  const navigate = useNavigate()

  const handleBack = () => navigate(-1)
  const handleHome = () => navigate('/')
  const handleRefresh = () => {
    if (onRetry) {
      onRetry()
    } else {
      window.location.reload()
    }
  }

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          py: 4,
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 6,
            textAlign: 'center',
            borderRadius: 3,
            maxWidth: 600,
          }}
        >
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              mb: 3,
            }}
          >
            <ErrorOutline
              sx={{
                fontSize: 120,
                color: 'error.main',
                opacity: 0.8,
              }}
            />
          </Box>

          {statusCode && (
            <Typography
              variant="h1"
              sx={{
                fontSize: '5rem',
                fontWeight: 700,
                color: 'text.secondary',
                mb: 2,
              }}
            >
              {statusCode}
            </Typography>
          )}

          <Typography
            variant="h4"
            gutterBottom
            sx={{ fontWeight: 600, mb: 2 }}
          >
            {title}
          </Typography>

          <Typography
            variant="body1"
            color="text.secondary"
            sx={{ mb: 4, lineHeight: 1.7 }}
          >
            {message}
          </Typography>

          <Box
            sx={{
              display: 'flex',
              gap: 2,
              justifyContent: 'center',
              flexWrap: 'wrap',
            }}
          >
            {showBackButton && (
              <Button
                variant="outlined"
                startIcon={<ArrowBack />}
                onClick={handleBack}
                size="large"
              >
                Go Back
              </Button>
            )}

            {showHomeButton && (
              <Button
                variant="contained"
                startIcon={<Home />}
                onClick={handleHome}
                size="large"
              >
                Go Home
              </Button>
            )}

            {showRefreshButton && (
              <Button
                variant="outlined"
                startIcon={<Refresh />}
                onClick={handleRefresh}
                size="large"
              >
                Try Again
              </Button>
            )}
          </Box>
        </Paper>
      </Box>
    </Container>
  )
}
