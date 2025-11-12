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
  Fade,
  Zoom,
  Grow,
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
      <Zoom in={true} timeout={400}>
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 8 }}>
          <CircularProgress size={60} thickness={4} />
          <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
            Loading analytics...
          </Typography>
        </Box>
      </Zoom>
    )
  }

  if (error) {
    return (
      <Fade in={true} timeout={600}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      </Fade>
    )
  }

  if (!stats) {
    return (
      <Fade in={true} timeout={600}>
        <Alert severity="info">
          No analytics data available yet. Start by uploading documents and asking questions!
        </Alert>
      </Fade>
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
      <Fade in={true} timeout={600}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            📊 Analytics
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Track your usage patterns and AI performance metrics
          </Typography>
        </Box>
      </Fade>

      {/* Overview Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Grow in={true} timeout={800}>
            <Card
              sx={{
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: 6,
                },
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box
                    sx={{
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      borderRadius: 2,
                      p: 1.5,
                      mr: 2,
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    <Description sx={{ fontSize: 32, color: 'white' }} />
                  </Box>
                  <Box>
                    <Typography variant="h3" fontWeight={700}>
                      {stats.total_documents}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total Documents
                    </Typography>
                  </Box>
                </Box>
                {stats.active_document && (
                  <Chip
                    label={`📄 Active: ${stats.active_document.file_name}`}
                    size="small"
                    color="primary"
                    sx={{ mt: 1, maxWidth: '100%' }}
                  />
                )}
              </CardContent>
            </Card>
          </Grow>
        </Grid>

        <Grid item xs={12} md={4}>
          <Grow in={true} timeout={1000}>
            <Card
              sx={{
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: 6,
                },
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box
                    sx={{
                      background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
                      borderRadius: 2,
                      p: 1.5,
                      mr: 2,
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    <QuestionAnswer sx={{ fontSize: 32, color: 'white' }} />
                  </Box>
                  <Box>
                    <Typography variant="h3" fontWeight={700}>
                      {stats.total_questions}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Questions Asked
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="caption" color="text.secondary">
                  💬 AI conversations completed
                </Typography>
              </CardContent>
            </Card>
          </Grow>
        </Grid>

        <Grid item xs={12} md={4}>
          <Grow in={true} timeout={1200}>
            <Card
              sx={{
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: 6,
                },
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box
                    sx={{
                      background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                      borderRadius: 2,
                      p: 1.5,
                      mr: 2,
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    <Speed sx={{ fontSize: 32, color: 'white' }} />
                  </Box>
                  <Box>
                    <Typography variant="h3" fontWeight={700}>
                      {((stats.avg_response_time_ms || 0) / 1000).toFixed(2)}s
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Avg Response Time
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="caption" color="text.secondary">
                  ⚡ Average AI processing time
                </Typography>
              </CardContent>
            </Card>
          </Grow>
        </Grid>
      </Grid>

      {/* Document Types Distribution */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Fade in={true} timeout={1400}>
            <Card
              sx={{
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 6,
                },
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <PieChartIcon sx={{ fontSize: 40, color: 'success.main', mr: 2 }} />
                  <Typography variant="h6" fontWeight={600}>
                    📈 Documents by Type
                  </Typography>
                </Box>

                {documentTypeData.length === 0 ? (
                  <Typography variant="body2" color="text.secondary">
                    No documents uploaded yet
                  </Typography>
                ) : (
                  <Box>
                    {documentTypeData.map((item, index) => (
                      <Grow key={item.type} in={true} timeout={1600 + index * 100}>
                        <Box sx={{ mb: 2 }}>
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
                              height: 10,
                              borderRadius: 5,
                              backgroundColor: 'grey.200',
                              '& .MuiLinearProgress-bar': {
                                backgroundColor: getTypeColor(item.type),
                                borderRadius: 5,
                                transition: 'transform 0.8s ease',
                              },
                            }}
                          />
                        </Box>
                      </Grow>
                    ))}
                  </Box>
                )}
              </CardContent>
            </Card>
          </Fade>
        </Grid>

        <Grid item xs={12} md={6}>
          <Fade in={true} timeout={1600}>
            <Card
              sx={{
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 6,
                },
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <Timeline sx={{ fontSize: 40, color: 'secondary.main', mr: 2 }} />
                  <Typography variant="h6" fontWeight={600}>
                    📋 Document Types Summary
                  </Typography>
                </Box>

                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell><strong>Type</strong></TableCell>
                        <TableCell align="right"><strong>Count</strong></TableCell>
                        <TableCell align="right"><strong>Share</strong></TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {documentTypeData.map((item, index) => (
                        <Grow key={item.type} in={true} timeout={1800 + index * 100}>
                          <TableRow
                            sx={{
                              transition: 'all 0.2s ease',
                              '&:hover': {
                                backgroundColor: 'action.hover',
                                transform: 'scale(1.02)',
                              },
                            }}
                          >
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
                            <TableCell align="right"><strong>{item.count}</strong></TableCell>
                            <TableCell align="right">
                              {item.percentage.toFixed(1)}%
                            </TableCell>
                          </TableRow>
                        </Grow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Fade>
        </Grid>

        {/* Performance Insights */}
        <Grid item xs={12}>
          <Fade in={true} timeout={1800}>
            <Card
              sx={{
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 6,
                },
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <TrendingUp sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                  <Typography variant="h6" fontWeight={600}>
                    🚀 Performance Insights
                  </Typography>
                </Box>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <Zoom in={true} timeout={2000}>
                      <Paper
                        sx={{
                          p: 3,
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          color: 'white',
                          transition: 'all 0.3s ease',
                          '&:hover': {
                            transform: 'scale(1.05)',
                            boxShadow: 6,
                          },
                        }}
                      >
                        <Typography variant="h4" fontWeight={700}>
                          {stats.total_questions > 0
                            ? (stats.total_questions / Math.max(stats.total_documents, 1)).toFixed(1)
                            : '0'}
                        </Typography>
                        <Typography variant="body1" sx={{ mt: 1 }}>
                          📊 Questions per Document
                        </Typography>
                      </Paper>
                    </Zoom>
                  </Grid>

                  <Grid item xs={12} md={4}>
                    <Zoom in={true} timeout={2200}>
                      <Paper
                        sx={{
                          p: 3,
                          background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
                          color: 'white',
                          transition: 'all 0.3s ease',
                          '&:hover': {
                            transform: 'scale(1.05)',
                            boxShadow: 6,
                          },
                        }}
                      >
                        <Typography variant="h4" fontWeight={700}>
                          {(stats.avg_response_time_ms || 0) / 1000 < 2 ? '⚡ Fast' : (stats.avg_response_time_ms || 0) / 1000 < 4 ? '🚀 Medium' : '🐌 Slow'}
                        </Typography>
                        <Typography variant="body1" sx={{ mt: 1 }}>
                          Response Speed Rating
                        </Typography>
                      </Paper>
                    </Zoom>
                  </Grid>

                  <Grid item xs={12} md={4}>
                    <Zoom in={true} timeout={2400}>
                      <Paper
                        sx={{
                          p: 3,
                          background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                          color: 'white',
                          transition: 'all 0.3s ease',
                          '&:hover': {
                            transform: 'scale(1.05)',
                            boxShadow: 6,
                          },
                        }}
                      >
                        <Typography variant="h4" fontWeight={700}>
                          {documentTypeData.length}
                        </Typography>
                        <Typography variant="body1" sx={{ mt: 1 }}>
                          📁 Different File Types
                        </Typography>
                      </Paper>
                    </Zoom>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Fade>
        </Grid>
      </Grid>
    </Box>
  )
}
