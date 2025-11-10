import { Box, Skeleton, Paper } from '@mui/material'

export interface ChatSkeletonProps {
  messages?: number
}

export default function ChatSkeleton({ messages = 5 }: ChatSkeletonProps) {
  return (
    <Box sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
      {/* Chat Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3, gap: 2 }}>
        <Skeleton variant="circular" width={48} height={48} />
        <Box sx={{ flex: 1 }}>
          <Skeleton variant="text" width="30%" height={24} />
          <Skeleton variant="text" width="20%" height={16} />
        </Box>
        <Skeleton variant="rectangular" width={100} height={36} sx={{ borderRadius: 1 }} />
      </Box>

      {/* Chat Messages */}
      <Box sx={{ mb: 3 }}>
        {[...Array(messages)].map((_, i) => {
          const isUser = i % 2 === 0
          return (
            <Box
              key={i}
              sx={{
                display: 'flex',
                justifyContent: isUser ? 'flex-end' : 'flex-start',
                mb: 2,
              }}
            >
              <Paper
                elevation={0}
                sx={{
                  p: 2,
                  maxWidth: '70%',
                  backgroundColor: isUser ? 'primary.main' : 'grey.100',
                  borderRadius: 2,
                  opacity: 0.7,
                }}
              >
                <Skeleton
                  variant="text"
                  height={20}
                  width={`${Math.random() * 40 + 60}%`}
                  sx={{
                    bgcolor: isUser ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.11)',
                  }}
                />
                <Skeleton
                  variant="text"
                  height={20}
                  width={`${Math.random() * 30 + 40}%`}
                  sx={{
                    bgcolor: isUser ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.11)',
                  }}
                />
              </Paper>
            </Box>
          )
        })}

        {/* Typing Indicator */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, ml: 2 }}>
          <Skeleton variant="circular" width={8} height={8} animation="wave" />
          <Skeleton variant="circular" width={8} height={8} animation="wave" sx={{ animationDelay: '0.2s' }} />
          <Skeleton variant="circular" width={8} height={8} animation="wave" sx={{ animationDelay: '0.4s' }} />
        </Box>
      </Box>

      {/* Chat Input */}
      <Paper elevation={2} sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Skeleton variant="circular" width={40} height={40} />
          <Skeleton variant="rectangular" sx={{ flex: 1 }} height={48} />
          <Skeleton variant="rectangular" width={100} height={48} sx={{ borderRadius: 1 }} />
        </Box>
      </Paper>
    </Box>
  )
}
