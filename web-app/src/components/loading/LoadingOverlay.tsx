import { Box, CircularProgress, Typography, Backdrop } from '@mui/material'

export interface LoadingOverlayProps {
  open: boolean
  message?: string
  transparent?: boolean
  blur?: boolean
}

export default function LoadingOverlay({
  open,
  message,
  transparent = false,
  blur = true,
}: LoadingOverlayProps) {
  return (
    <Backdrop
      open={open}
      sx={{
        color: '#fff',
        zIndex: (theme) => theme.zIndex.modal + 1,
        backgroundColor: transparent ? 'rgba(0, 0, 0, 0.3)' : 'rgba(0, 0, 0, 0.7)',
        backdropFilter: blur ? 'blur(4px)' : 'none',
      }}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 2,
        }}
      >
        <CircularProgress size={60} thickness={4} />
        {message && (
          <Typography variant="h6" sx={{ mt: 2, fontWeight: 500 }}>
            {message}
          </Typography>
        )}
      </Box>
    </Backdrop>
  )
}
