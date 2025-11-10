import { useState } from 'react'
import { Button, CircularProgress, Box, Typography } from '@mui/material'
import { Refresh } from '@mui/icons-material'

export interface RetryButtonProps {
  onRetry: () => Promise<void> | void
  text?: string
  loadingText?: string
  variant?: 'text' | 'outlined' | 'contained'
  size?: 'small' | 'medium' | 'large'
  fullWidth?: boolean
  showAttempts?: boolean
  maxAttempts?: number
}

export default function RetryButton({
  onRetry,
  text = 'Try Again',
  loadingText = 'Retrying...',
  variant = 'contained',
  size = 'medium',
  fullWidth = false,
  showAttempts = false,
  maxAttempts = 3,
}: RetryButtonProps) {
  const [isRetrying, setIsRetrying] = useState(false)
  const [attempts, setAttempts] = useState(0)

  const handleClick = async () => {
    if (isRetrying) return

    setIsRetrying(true)
    setAttempts(prev => prev + 1)

    try {
      await onRetry()
    } catch (error) {
      console.error('Retry failed:', error)
    } finally {
      setIsRetrying(false)
    }
  }

  const isMaxAttemptsReached = showAttempts && attempts >= maxAttempts

  return (
    <Box>
      <Button
        variant={variant}
        size={size}
        fullWidth={fullWidth}
        onClick={handleClick}
        disabled={isRetrying || isMaxAttemptsReached}
        startIcon={
          isRetrying ? (
            <CircularProgress size={20} color="inherit" />
          ) : (
            <Refresh />
          )
        }
        sx={{
          minWidth: 140,
          '& .MuiButton-startIcon': {
            animation: isRetrying ? 'spin 1s linear infinite' : 'none',
          },
          '@keyframes spin': {
            '0%': {
              transform: 'rotate(0deg)',
            },
            '100%': {
              transform: 'rotate(360deg)',
            },
          },
        }}
      >
        {isRetrying ? loadingText : text}
      </Button>

      {showAttempts && attempts > 0 && (
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ mt: 1, display: 'block', textAlign: 'center' }}
        >
          {isMaxAttemptsReached
            ? `Maximum attempts reached (${attempts}/${maxAttempts})`
            : `Attempt ${attempts}/${maxAttempts}`}
        </Typography>
      )}
    </Box>
  )
}
