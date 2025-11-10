import { Card, CardContent, Skeleton, Box } from '@mui/material'

export interface CardSkeletonProps {
  variant?: 'simple' | 'with-image' | 'with-actions'
  height?: number | string
  width?: number | string
}

export default function CardSkeleton({
  variant = 'simple',
  height,
  width,
}: CardSkeletonProps) {
  if (variant === 'with-image') {
    return (
      <Card sx={{ height, width }}>
        <Skeleton variant="rectangular" height={200} />
        <CardContent>
          <Skeleton variant="text" height={32} width="80%" sx={{ mb: 1 }} />
          <Skeleton variant="text" height={20} width="60%" sx={{ mb: 2 }} />
          <Skeleton variant="text" height={16} />
          <Skeleton variant="text" height={16} width="90%" />
        </CardContent>
      </Card>
    )
  }

  if (variant === 'with-actions') {
    return (
      <Card sx={{ height, width }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Skeleton variant="text" height={32} width="60%" />
            <Skeleton variant="circular" width={40} height={40} />
          </Box>
          <Skeleton variant="text" height={20} width="40%" sx={{ mb: 2 }} />
          <Skeleton variant="rectangular" height={100} sx={{ mb: 2, borderRadius: 1 }} />
          <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
            <Skeleton variant="rectangular" width={80} height={36} sx={{ borderRadius: 1 }} />
            <Skeleton variant="rectangular" width={80} height={36} sx={{ borderRadius: 1 }} />
          </Box>
        </CardContent>
      </Card>
    )
  }

  // Simple variant
  return (
    <Card sx={{ height, width }}>
      <CardContent>
        <Skeleton variant="text" height={32} width="70%" sx={{ mb: 1 }} />
        <Skeleton variant="text" height={20} width="50%" sx={{ mb: 2 }} />
        <Skeleton variant="text" height={16} />
        <Skeleton variant="text" height={16} width="95%" />
        <Skeleton variant="text" height={16} width="80%" />
      </CardContent>
    </Card>
  )
}
