import { useEffect, useState } from 'react'
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  LinearProgress,
  Chip,
  Fade,
} from '@mui/material'
import {
  TrendingUp,
  Description,
  Chat,
  Speed,
  Upload,
  PsychologyAlt,
} from '@mui/icons-material'
import { useNavigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { RootState } from '@/store'
import { analyticsApi } from '@/api/services'
import StatsCards from '@/components/analytics/StatsCards'

interface DashboardStats {
  total_questions: number
  total_documents: number
  avg_response_time: number
  documents_today: number
  questions_today: number
  activity_chart: Array<{ date: string; questions: number }>
  recent_documents: Array<any>
  is_premium: boolean
}

export default function DashboardPage() {
  const navigate = useNavigate()
  const { user } = useSelector((state: RootState) => state.auth)
  const [stats, setStats] = useState<DashboardStats>({
    total_questions: 0,
    total_documents: 0,
    avg_response_time: 0,
    documents_today: 0,
    questions_today: 0,
    activity_chart: [],
    recent_documents: [],
    is_premium: false,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardStats()
  }, [])

  const fetchDashboardStats = async () => {
    try {
      const response = await analyticsApi.getUserStats()
      setStats({
        total_questions: response.total_questions,
        total_documents: response.total_documents,
        avg_response_time: response.avg_response_time_ms || 0,
        documents_today: 0,
        questions_today: 0,
        activity_chart: [],
        recent_documents: [],
        is_premium: user?.role === 'premium' || false,
      })
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: 'Total Documents',
      value: stats.total_documents,
      icon: <Description sx={{ fontSize: 40 }} />,
      color: '#1976d2',
      subtitle: `${stats.documents_today} uploaded today`,
    },
    {
      title: 'Questions Asked',
      value: stats.total_questions,
      icon: <Chat sx={{ fontSize: 40 }} />,
      color: '#2e7d32',
      subtitle: `${stats.questions_today} asked today`,
    },
    {
      title: 'Avg Response Time',
      value: stats.avg_response_time ? `${stats.avg_response_time.toFixed(2)}s` : '0s',
      icon: <Speed sx={{ fontSize: 40 }} />,
      color: '#ed6c02',
      subtitle: 'Average AI response',
    },
    {
      title: 'Recent Documents',
      value: stats.recent_documents.length,
      icon: <PsychologyAlt sx={{ fontSize: 40 }} />,
      color: '#9c27b0',
      subtitle: 'Last uploaded',
    },
  ]

  if (loading) {
    return <LinearProgress />
  }

  return (
    <Box>
      <Fade in={true} timeout={800}>
        <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              Welcome back, {user?.first_name || user?.username}! 👋
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Here's an overview of your AI business intelligence activities
            </Typography>
          </Box>
          {user?.is_premium && (
            <Chip
              label="✨ Premium"
              color="primary"
              icon={<TrendingUp />}
              sx={{
                fontWeight: 600,
                fontSize: '0.9rem',
                height: 36,
                px: 1,
              }}
            />
          )}
        </Box>
      </Fade>

      <Fade in={true} timeout={1000}>
        <Box>
          <StatsCards
            totalDocuments={stats.total_documents}
            questionsAsked={stats.total_questions}
            avgResponseTime={stats.avg_response_time ? `${(stats.avg_response_time / 1000).toFixed(2)}s` : 'N/A'}
            accuracy={95}
          />
        </Box>
      </Fade>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Fade in={true} timeout={1200}>
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
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  🚀 Quick Actions
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
                  <Button
                    variant="contained"
                    startIcon={<Upload />}
                    onClick={() => navigate('/documents')}
                    fullWidth
                    sx={{
                      py: 1.5,
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        transform: 'scale(1.02)',
                        boxShadow: 4,
                      },
                    }}
                  >
                    Upload Document
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<Chat />}
                    onClick={() => navigate('/chat')}
                    fullWidth
                    sx={{
                      py: 1.5,
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        transform: 'scale(1.02)',
                      },
                    }}
                  >
                    Start AI Chat
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<TrendingUp />}
                    onClick={() => navigate('/analytics')}
                    fullWidth
                    sx={{
                      py: 1.5,
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        transform: 'scale(1.02)',
                      },
                    }}
                  >
                    View Analytics
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Fade>
        </Grid>

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
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  📄 Recent Documents
                </Typography>
                <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {stats.recent_documents.length === 0 ? (
                    <Box sx={{ textAlign: 'center', py: 3 }}>
                      <Description sx={{ fontSize: 48, color: 'text.secondary', mb: 1 }} />
                      <Typography variant="body2" color="text.secondary">
                        No documents uploaded yet
                      </Typography>
                    </Box>
                  ) : (
                    stats.recent_documents.map((doc) => (
                      <Box
                        key={doc.id}
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          p: 1.5,
                          borderRadius: 1,
                          transition: 'all 0.2s ease',
                          '&:hover': {
                            backgroundColor: 'action.hover',
                            transform: 'translateX(4px)',
                          },
                        }}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Description color="primary" />
                          <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                            {doc.file_name}
                          </Typography>
                        </Box>
                        {doc.is_active && (
                          <Chip label="Active" size="small" color="primary" />
                        )}
                      </Box>
                    ))
                  )}
                </Box>
              </CardContent>
            </Card>
          </Fade>
        </Grid>
      </Grid>

      {!user?.is_premium && (
        <Fade in={true} timeout={1600}>
          <Card
            sx={{
              mt: 3,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              position: 'relative',
              overflow: 'hidden',
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: 8,
              },
              '&::before': {
                content: '""',
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'radial-gradient(circle at 30% 50%, rgba(255,255,255,0.1), transparent)',
              },
            }}
          >
            <CardContent>
              <Box sx={{ color: 'white', textAlign: 'center', py: 2, position: 'relative' }}>
                <Typography variant="h5" fontWeight={700} gutterBottom>
                  ✨ Upgrade to Premium
                </Typography>
                <Typography variant="body1" sx={{ mb: 3, opacity: 0.95 }}>
                  Unlock unlimited documents, faster processing, and advanced analytics
                </Typography>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/premium')}
                  sx={{
                    backgroundColor: 'white',
                    color: '#667eea',
                    fontWeight: 600,
                    px: 4,
                    py: 1.5,
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      backgroundColor: 'rgba(255,255,255,0.95)',
                      transform: 'scale(1.05)',
                      boxShadow: 4,
                    },
                  }}
                >
                  Learn More
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Fade>
      )}
    </Box>
  )
}
