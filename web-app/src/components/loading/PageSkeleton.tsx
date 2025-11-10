import { Box, Skeleton, Container, Grid } from '@mui/material'

export interface PageSkeletonProps {
  variant?: 'dashboard' | 'list' | 'detail' | 'form'
  rows?: number
}

export default function PageSkeleton({ variant = 'list', rows = 5 }: PageSkeletonProps) {
  if (variant === 'dashboard') {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Header */}
        <Skeleton variant="rectangular" width="60%" height={40} sx={{ mb: 3 }} />

        {/* Stats Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {[1, 2, 3, 4].map((i) => (
            <Grid item xs={12} sm={6} md={3} key={i}>
              <Skeleton variant="rectangular" height={120} sx={{ borderRadius: 2 }} />
            </Grid>
          ))}
        </Grid>

        {/* Chart */}
        <Skeleton variant="rectangular" height={300} sx={{ borderRadius: 2, mb: 3 }} />

        {/* Table */}
        <Skeleton variant="rectangular" height={200} sx={{ borderRadius: 2 }} />
      </Container>
    )
  }

  if (variant === 'detail') {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Breadcrumb */}
        <Skeleton variant="text" width="30%" height={24} sx={{ mb: 3 }} />

        {/* Title */}
        <Skeleton variant="rectangular" width="50%" height={48} sx={{ mb: 3 }} />

        {/* Content */}
        <Box sx={{ display: 'flex', gap: 3 }}>
          <Box sx={{ flex: 1 }}>
            {[...Array(6)].map((_, i) => (
              <Skeleton key={i} variant="text" height={28} sx={{ mb: 2 }} />
            ))}
          </Box>
          <Skeleton variant="rectangular" width={300} height={400} sx={{ borderRadius: 2 }} />
        </Box>
      </Container>
    )
  }

  if (variant === 'form') {
    return (
      <Container maxWidth="sm" sx={{ py: 4 }}>
        {/* Title */}
        <Skeleton variant="text" width="60%" height={40} sx={{ mb: 4 }} />

        {/* Form Fields */}
        {[...Array(rows)].map((_, i) => (
          <Box key={i} sx={{ mb: 3 }}>
            <Skeleton variant="text" width="30%" height={24} sx={{ mb: 1 }} />
            <Skeleton variant="rectangular" height={56} sx={{ borderRadius: 1 }} />
          </Box>
        ))}

        {/* Buttons */}
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 4 }}>
          <Skeleton variant="rectangular" width={100} height={42} sx={{ borderRadius: 1 }} />
          <Skeleton variant="rectangular" width={100} height={42} sx={{ borderRadius: 1 }} />
        </Box>
      </Container>
    )
  }

  // Default: list variant
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header with action button */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Skeleton variant="text" width="40%" height={40} />
        <Skeleton variant="rectangular" width={120} height={40} sx={{ borderRadius: 1 }} />
      </Box>

      {/* Search/Filter bar */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <Skeleton variant="rectangular" sx={{ flex: 1 }} height={56} />
        <Skeleton variant="rectangular" width={120} height={56} />
      </Box>

      {/* List items */}
      {[...Array(rows)].map((_, i) => (
        <Skeleton
          key={i}
          variant="rectangular"
          height={80}
          sx={{ borderRadius: 2, mb: 2 }}
        />
      ))}

      {/* Pagination */}
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <Skeleton variant="rectangular" width={300} height={40} sx={{ borderRadius: 1 }} />
      </Box>
    </Container>
  )
}
