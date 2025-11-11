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
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Welcome back, {user?.first_name || user?.username}!
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Here's an overview of your AI business intelligence activities
          </Typography>
        </Box>
        {user?.is_premium && (
          <Chip
            label="Premium"
            color="primary"
            icon={<TrendingUp />}
            sx={{ fontWeight: 600 }}
          />
        )}
      </Box>

      <Grid container spacing={3}>
        {statCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                },
              }}
            >
              <CardContent>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    mb: 2,
                  }}
                >
                  <Typography variant="h6" color="text.secondary">
                    {card.title}
                  </Typography>
                  <Box sx={{ color: card.color }}>{card.icon}</Box>
                </Box>
                <Typography variant="h3" fontWeight={700} gutterBottom>
                  {card.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {card.subtitle}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Quick Actions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
                <Button
                  variant="contained"
                  startIcon={<Upload />}
                  onClick={() => navigate('/documents')}
                  fullWidth
                >
                  Upload Document
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Chat />}
                  onClick={() => navigate('/chat')}
                  fullWidth
                >
                  Start AI Chat
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<TrendingUp />}
                  onClick={() => navigate('/analytics')}
                  fullWidth
                >
                  View Analytics
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Recent Documents
              </Typography>
              <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 1 }}>
                {stats.recent_documents.length === 0 ? (
                  <Typography variant="body2" color="text.secondary">
                    No documents uploaded yet
                  </Typography>
                ) : (
                  stats.recent_documents.map((doc) => (
                    <Box
                      key={doc.id}
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        p: 1,
                        borderRadius: 1,
                        '&:hover': { backgroundColor: 'action.hover' },
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
        </Grid>
      </Grid>

      {!user?.is_premium && (
        <Card sx={{ mt: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <CardContent>
            <Box sx={{ color: 'white', textAlign: 'center', py: 2 }}>
              <Typography variant="h5" fontWeight={700} gutterBottom>
                Upgrade to Premium
              </Typography>
              <Typography variant="body1" sx={{ mb: 3 }}>
                Unlock unlimited documents, faster processing, and advanced analytics
              </Typography>
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/premium')}
                sx={{
                  backgroundColor: 'white',
                  color: '#667eea',
                  '&:hover': {
                    backgroundColor: 'rgba(255,255,255,0.9)',
                  },
                }}
              >
                Learn More
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  )
}
