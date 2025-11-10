import { Box, Button, Typography, Paper } from '@mui/material'
import {
  CloudOff,
  Refresh,
  Settings,
} from '@mui/icons-material'

export interface NetworkErrorProps {
  onRetry?: () => void
  showSettings?: boolean
}

export default function NetworkError({
  onRetry,
  showSettings = false,
}: NetworkErrorProps) {
  const handleRetry = () => {
    if (onRetry) {
      onRetry()
    } else {
      window.location.reload()
    }
  }

  const handleSettings = () => {
    // Open network settings or help
    window.open('https://support.google.com/chrome/answer/95617', '_blank')
  }

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '400px',
        p: 3,
      }}
    >
      <Paper
        elevation={0}
        sx={{
          p: 4,
          textAlign: 'center',
          maxWidth: 500,
          backgroundColor: 'background.default',
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 2,
        }}
      >
        <CloudOff
          sx={{
            fontSize: 80,
            color: 'text.secondary',
            opacity: 0.5,
            mb: 3,
          }}
        />

        <Typography
          variant="h5"
          gutterBottom
          sx={{ fontWeight: 600, mb: 2 }}
        >
          No Internet Connection
        </Typography>

        <Typography
          variant="body1"
          color="text.secondary"
          sx={{ mb: 3, lineHeight: 1.7 }}
        >
          Please check your network connection and try again.
          Make sure you're connected to the internet.
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
          <Button
            variant="contained"
            startIcon={<Refresh />}
            onClick={handleRetry}
            size="large"
          >
            Retry
          </Button>

          {showSettings && (
            <Button
              variant="outlined"
              startIcon={<Settings />}
              onClick={handleSettings}
              size="large"
            >
              Network Settings
            </Button>
          )}
        </Box>

        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ mt: 3, display: 'block' }}
        >
          Troubleshooting tips:
        </Typography>
        <Typography
          variant="caption"
          color="text.secondary"
          component="div"
          sx={{ mt: 1, textAlign: 'left', maxWidth: 350, mx: 'auto' }}
        >
          • Check if your Wi-Fi or cellular data is enabled
          <br />
          • Try disabling VPN or proxy if you're using one
          <br />
          • Restart your router or modem
          <br />
          • Contact your network administrator if on corporate network
        </Typography>
      </Paper>
    </Box>
  )
}
