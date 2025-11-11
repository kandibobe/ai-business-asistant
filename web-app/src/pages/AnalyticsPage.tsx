import { useEffect, useState } from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert,
  Chip,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material'
import {
  Timeline,
  PieChart as PieChartIcon,
  TrendingUp,
  Description,
  Speed,
  QuestionAnswer,
} from '@mui/icons-material'
import { analyticsApi, UserStatsResponse } from '@/api/services'

interface UserStats extends UserStatsResponse {
  active_document?: {
    id: number
    file_name: string
    document_type: string
  }
}

export default function AnalyticsPage() {
  const [stats, setStats] = useState<UserStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      setLoading(true)
      const response = await analyticsApi.getUserStats()
      setStats(response)
    } catch (err: any) {
      console.error('Failed to load analytics:', err)
      setError(err.message || 'Failed to load analytics')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error}
      </Alert>
    )
  }

  if (!stats) {
    return (
      <Alert severity="info">
        No analytics data available yet. Start by uploading documents and asking questions!
      </Alert>
    )
  }

  // Calculate percentages for document types
  const totalDocs = Object.values(stats.documents_by_type).reduce((a, b) => a + b, 0)
  const documentTypeData = Object.entries(stats.documents_by_type).map(([type, count]) => ({
    type,
    count,
    percentage: totalDocs > 0 ? (count / totalDocs) * 100 : 0,
  }))

  const getTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      pdf: '#d32f2f',
      excel: '#2e7d32',
      word: '#1976d2',
      audio: '#9c27b0',
      text: '#ed6c02',
    }
    return colors[type] || '#757575'
  }

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Analytics
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Track your usage patterns and AI performance metrics
        </Typography>
      </Box>

      {/* Overview Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Description sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                <Box>
                  <Typography variant="h4" fontWeight={700}>
                    {stats.total_documents}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Documents
                  </Typography>
                </Box>
              </Box>
              {stats.active_document && (
                <Chip
                  label={`Active: ${stats.active_document.file_name}`}
                  size="small"
                  color="primary"
                  sx={{ mt: 1 }}
                />
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <QuestionAnswer sx={{ fontSize: 40, color: 'success.main', mr: 2 }} />
                <Box>
                  <Typography variant="h4" fontWeight={700}>
                    {stats.total_questions}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Questions Asked
                  </Typography>
                </Box>
              </Box>
              <Typography variant="caption" color="text.secondary">
                AI conversations completed
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Speed sx={{ fontSize: 40, color: 'warning.main', mr: 2 }} />
                <Box>
                  <Typography variant="h4" fontWeight={700}>
                    {((stats.avg_response_time_ms || 0) / 1000).toFixed(2)}s
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Avg Response Time
                  </Typography>
                </Box>
              </Box>
              <Typography variant="caption" color="text.secondary">
                Average AI processing time
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Document Types Distribution */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <PieChartIcon sx={{ fontSize: 40, color: 'success.main', mr: 2 }} />
                <Typography variant="h6" fontWeight={600}>
                  Documents by Type
                </Typography>
              </Box>

              {documentTypeData.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No documents uploaded yet
                </Typography>
              ) : (
                <Box>
                  {documentTypeData.map((item) => (
                    <Box key={item.type} sx={{ mb: 2 }}>
                      <Box
                        sx={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          mb: 0.5,
                        }}
                      >
                        <Typography variant="body2" fontWeight={600}>
                          {item.type.toUpperCase()}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {item.count} ({item.percentage.toFixed(0)}%)
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={item.percentage}
                        sx={{
                          height: 8,
                          borderRadius: 4,
                          backgroundColor: 'grey.200',
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: getTypeColor(item.type),
                          },
                        }}
                      />
                    </Box>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Timeline sx={{ fontSize: 40, color: 'secondary.main', mr: 2 }} />
                <Typography variant="h6" fontWeight={600}>
                  Document Types Summary
                </Typography>
              </Box>

              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Type</TableCell>
                      <TableCell align="right">Count</TableCell>
                      <TableCell align="right">Share</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {documentTypeData.map((item) => (
                      <TableRow key={item.type}>
                        <TableCell>
                          <Chip
                            label={item.type.toUpperCase()}
                            size="small"
                            sx={{
                              backgroundColor: getTypeColor(item.type),
                              color: 'white',
                              fontWeight: 600,
                            }}
                          />
                        </TableCell>
                        <TableCell align="right">{item.count}</TableCell>
                        <TableCell align="right">
                          {item.percentage.toFixed(1)}%
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Performance Insights */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <TrendingUp sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                <Typography variant="h6" fontWeight={600}>
                  Performance Insights
                </Typography>
              </Box>

              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, backgroundColor: 'primary.light', color: 'white' }}>
                    <Typography variant="h5" fontWeight={700}>
                      {stats.total_questions > 0
                        ? (stats.total_questions / Math.max(stats.total_documents, 1)).toFixed(1)
                        : '0'}
                    </Typography>
                    <Typography variant="body2">
                      Questions per Document
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, backgroundColor: 'success.light', color: 'white' }}>
                    <Typography variant="h5" fontWeight={700}>
                      {(stats.avg_response_time_ms || 0) / 1000 < 2 ? 'Fast' : (stats.avg_response_time_ms || 0) / 1000 < 4 ? 'Medium' : 'Slow'}
                    </Typography>
                    <Typography variant="body2">
                      Response Speed Rating
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, backgroundColor: 'warning.light', color: 'white' }}>
                    <Typography variant="h5" fontWeight={700}>
                      {documentTypeData.length}
                    </Typography>
                    <Typography variant="body2">
                      Different File Types
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}
