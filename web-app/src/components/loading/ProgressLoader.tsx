import { Box, LinearProgress, Typography } from '@mui/material'

export interface ProgressLoaderProps {
  progress: number
  message?: string
  showPercentage?: boolean
  color?: 'primary' | 'secondary' | 'success' | 'error' | 'info' | 'warning'
  height?: number
}

export default function ProgressLoader({
  progress,
  message,
  showPercentage = true,
  color = 'primary',
  height = 8,
}: ProgressLoaderProps) {
  const clampedProgress = Math.min(Math.max(progress, 0), 100)

  return (
    <Box sx={{ width: '100%' }}>
      {(message || showPercentage) && (
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          {message && (
            <Typography variant="body2" color="text.secondary">
              {message}
            </Typography>
          )}
          {showPercentage && (
            <Typography variant="body2" color="text.secondary" fontWeight={600}>
              {Math.round(clampedProgress)}%
            </Typography>
          )}
        </Box>
      )}
      <LinearProgress
        variant="determinate"
        value={clampedProgress}
        color={color}
        sx={{
          height,
          borderRadius: height / 2,
          backgroundColor: 'grey.200',
          '& .MuiLinearProgress-bar': {
            borderRadius: height / 2,
          },
        }}
      />
    </Box>
  )
}
