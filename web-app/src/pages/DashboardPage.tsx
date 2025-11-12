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
  Stack,
  Avatar,
  Divider,
  IconButton,
  alpha,
  Fade,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
} from '@mui/material'
import {
  TrendingUp,
  Description,
  Chat,
  Speed,
  Upload,
  PsychologyAlt,
  Assessment,
  Settings,
  ArrowForward,
  CheckCircle,
  AutoAwesome,
  InsertDriveFile,
  Forum,
  Timer,
  WorkspacePremium,
  TrendingDown,
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
      icon: <InsertDriveFile sx={{ fontSize: 32 }} />,
      gradient: gradients.primary,
      subtitle: `${stats.documents_today} uploaded today`,
      trend: stats.documents_today > 0 ? '+' + stats.documents_today : '0',
      trendUp: stats.documents_today > 0,
    },
    {
      title: 'AI Conversations',
      value: stats.total_questions,
      icon: <Forum sx={{ fontSize: 32 }} />,
      gradient: gradients.success,
      subtitle: `${stats.questions_today} questions today`,
      trend: stats.questions_today > 0 ? '+' + stats.questions_today : '0',
      trendUp: stats.questions_today > 0,
    },
    {
      title: 'Response Time',
      value: stats.avg_response_time ? `${stats.avg_response_time.toFixed(1)}s` : '0s',
      icon: <Timer sx={{ fontSize: 32 }} />,
      gradient: gradients.warning,
      subtitle: 'Average AI response',
      trend: stats.avg_response_time < 2 ? 'Fast' : 'Normal',
      trendUp: stats.avg_response_time < 2,
    },
    {
      title: 'AI Insights',
      value: stats.recent_documents.length,
      icon: <AutoAwesome sx={{ fontSize: 32 }} />,
      gradient: gradients.info,
      subtitle: 'Documents analyzed',
      trend: stats.recent_documents.length + ' active',
      trendUp: true,
    },
  ]

  const quickActions = [
    {
      title: 'Upload Documents',
      description: 'Add new files for AI analysis',
      icon: <Upload />,
      color: gradients.primary,
      path: '/app/documents',
    },
    {
      title: 'AI Chat',
      description: 'Ask questions about your documents',
      icon: <Chat />,
      color: gradients.success,
      path: '/app/chat',
    },
    {
      title: 'View Analytics',
      description: 'Detailed insights and reports',
      icon: <Assessment />,
      color: gradients.info,
      path: '/app/analytics',
    },
    {
      title: 'Settings',
      description: 'Customize your preferences',
      icon: <Settings />,
      color: gradients.warning,
      path: '/app/settings',
    },
  ]

  if (loading) {
    return (
      <Box sx={{ width: '100%' }}>
        <LinearProgress />
      </Box>
    )
  }

  return (
    <Box>
      {/* Welcome Header */}
      <Box sx={{ mb: 4 }}>
        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          justifyContent="space-between"
          alignItems={{ xs: 'flex-start', sm: 'center' }}
          spacing={2}
        >
          <Box>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              Welcome back, {user?.first_name || user?.username}! 👋
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Here's what's happening with your AI assistant today
            </Typography>
          </Box>
          {user?.is_premium && (
            <Chip
              label="Premium Member"
              color="primary"
              icon={<WorkspacePremium />}
              sx={{
                fontWeight: 600,
                px: 1,
                height: 40,
                background: gradients.royal,
                color: '#fff',
                '& .MuiChip-icon': {
                  color: '#fff',
                },
              }}
            />
          )}
        </Stack>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {statCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Fade in timeout={300 + index * 100}>
              <Card
                sx={{
                  height: '100%',
                  background: card.gradient,
                  color: '#fff',
                  position: 'relative',
                  overflow: 'hidden',
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: '0 12px 40px rgba(0,0,0,0.15)',
                  },
                }}
              >
                <CardContent sx={{ position: 'relative', zIndex: 1 }}>
                  <Stack spacing={2}>
                    <Box
                      sx={{
                        width: 56,
                        height: 56,
                        borderRadius: 3,
                        bgcolor: alpha('#fff', 0.2),
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      {card.icon}
                    </Box>
                    <Box>
                      <Typography variant="body2" sx={{ opacity: 0.9, mb: 0.5 }}>
                        {card.title}
                      </Typography>
                      <Typography variant="h3" fontWeight={700}>
                        {card.value}
                      </Typography>
                    </Box>
                    <Stack direction="row" alignItems="center" spacing={1}>
                      <Chip
                        size="small"
                        icon={card.trendUp ? <TrendingUp /> : <TrendingDown />}
                        label={card.trend}
                        sx={{
                          bgcolor: alpha('#fff', 0.2),
                          color: '#fff',
                          fontWeight: 600,
                          '& .MuiChip-icon': {
                            color: '#fff',
                          },
                        }}
                      />
                      <Typography variant="caption" sx={{ opacity: 0.8 }}>
                        {card.subtitle}
                      </Typography>
                    </Stack>
                  </Stack>
                </CardContent>
                {/* Background decoration */}
                <Box
                  sx={{
                    position: 'absolute',
                    top: -20,
                    right: -20,
                    width: 120,
                    height: 120,
                    borderRadius: '50%',
                    bgcolor: alpha('#fff', 0.1),
                  }}
                />
              </Card>
            </Fade>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Quick Actions */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Quick Actions
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Common tasks to get you started
              </Typography>
              <Grid container spacing={2}>
                {quickActions.map((action, index) => (
                  <Grid item xs={12} sm={6} key={index}>
                    <Card
                      sx={{
                        cursor: 'pointer',
                        transition: 'all 0.3s',
                        border: '1px solid',
                        borderColor: 'divider',
                        '&:hover': {
                          borderColor: 'primary.main',
                          transform: 'translateY(-4px)',
                          boxShadow: '0 8px 20px rgba(0,0,0,0.1)',
                        },
                      }}
                      onClick={() => navigate(action.path)}
                    >
                      <CardContent sx={{ p: 2.5 }}>
                        <Stack direction="row" spacing={2} alignItems="flex-start">
                          <Box
                            sx={{
                              width: 48,
                              height: 48,
                              borderRadius: 2,
                              background: action.color,
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              color: '#fff',
                              flexShrink: 0,
                            }}
                          >
                            {action.icon}
                          </Box>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="subtitle1" fontWeight={600} gutterBottom>
                              {action.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {action.description}
                            </Typography>
                          </Box>
                          <ArrowForward
                            sx={{ color: 'text.secondary', opacity: 0.5, mt: 1 }}
                          />
                        </Stack>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Documents */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 3 }}>
              <Stack
                direction="row"
                justifyContent="space-between"
                alignItems="center"
                sx={{ mb: 2 }}
              >
                <Typography variant="h6" fontWeight={600}>
                  Recent Documents
                </Typography>
                <IconButton
                  size="small"
                  onClick={() => navigate('/app/documents')}
                  sx={{ color: 'primary.main' }}
                >
                  <ArrowForward />
                </IconButton>
              </Stack>

              {stats.recent_documents.length === 0 ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Description
                    sx={{ fontSize: 48, color: 'text.secondary', opacity: 0.5, mb: 1 }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    No documents uploaded yet
                  </Typography>
                  <Button
                    variant="contained"
                    size="small"
                    startIcon={<Upload />}
                    onClick={() => navigate('/app/documents')}
                    sx={{ mt: 2 }}
                  >
                    Upload Now
                  </Button>
                </Box>
              ) : (
                <List sx={{ p: 0 }}>
                  {stats.recent_documents.slice(0, 5).map((doc, index) => (
                    <Box key={doc.id}>
                      {index > 0 && <Divider sx={{ my: 1 }} />}
                      <ListItem
                        sx={{
                          px: 0,
                          borderRadius: 1,
                          transition: 'all 0.2s',
                          '&:hover': {
                            bgcolor: 'action.hover',
                          },
                        }}
                      >
                        <ListItemIcon>
                          <Avatar
                            sx={{
                              width: 40,
                              height: 40,
                              background: gradients.primary,
                            }}
                          >
                            <Description />
                          </Avatar>
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="body2" fontWeight={600} noWrap>
                              {doc.file_name}
                            </Typography>
                          }
                          secondary={
                            <Typography variant="caption" color="text.secondary">
                              {new Date(doc.uploaded_at).toLocaleDateString()}
                            </Typography>
                          }
                        />
                        {doc.is_active && (
                          <CheckCircle sx={{ color: 'success.main', fontSize: 20 }} />
                        )}
                      </ListItem>
                    </Box>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Activity Summary */}
        <Grid item xs={12}>
          <Card>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Today's Activity
              </Typography>
              <Grid container spacing={3} sx={{ mt: 1 }}>
                <Grid item xs={12} sm={4}>
                  <Stack spacing={1}>
                    <Stack direction="row" alignItems="center" spacing={1}>
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: 'primary.main',
                        }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        Documents Uploaded
                      </Typography>
                    </Stack>
                    <Typography variant="h4" fontWeight={700}>
                      {stats.documents_today}
                    </Typography>
                  </Stack>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Stack spacing={1}>
                    <Stack direction="row" alignItems="center" spacing={1}>
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: 'success.main',
                        }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        Questions Asked
                      </Typography>
                    </Stack>
                    <Typography variant="h4" fontWeight={700}>
                      {stats.questions_today}
                    </Typography>
                  </Stack>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Stack spacing={1}>
                    <Stack direction="row" alignItems="center" spacing={1}>
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: 'warning.main',
                        }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        AI Insights Generated
                      </Typography>
                    </Stack>
                    <Typography variant="h4" fontWeight={700}>
                      {stats.total_questions}
                    </Typography>
                  </Stack>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Premium Upsell */}
      {!user?.is_premium && (
        <Fade in timeout={1000}>
          <Card
            sx={{
              mt: 4,
              background: gradients.royal,
              color: '#fff',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            <CardContent sx={{ p: 4, position: 'relative', zIndex: 1 }}>
              <Grid container spacing={3} alignItems="center">
                <Grid item xs={12} md={8}>
                  <Stack spacing={2}>
                    <Chip
                      icon={<WorkspacePremium />}
                      label="Premium"
                      size="small"
                      sx={{
                        width: 'fit-content',
                        bgcolor: alpha('#fff', 0.2),
                        color: '#fff',
                        fontWeight: 600,
                        '& .MuiChip-icon': {
                          color: '#fff',
                        },
                      }}
                    />
                    <Typography variant="h4" fontWeight={700}>
                      Unlock the Full Power of AI
                    </Typography>
                    <Typography variant="body1" sx={{ opacity: 0.9 }}>
                      Upgrade to Premium for unlimited documents, faster AI processing,
                      advanced analytics, and priority support.
                    </Typography>
                    <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
                      <Button
                        variant="contained"
                        size="large"
                        onClick={() => navigate('/app/premium')}
                        sx={{
                          bgcolor: '#fff',
                          color: 'primary.main',
                          '&:hover': {
                            bgcolor: alpha('#fff', 0.9),
                          },
                        }}
                      >
                        Upgrade Now
                      </Button>
                      <Button
                        variant="outlined"
                        size="large"
                        sx={{
                          borderColor: '#fff',
                          color: '#fff',
                          '&:hover': {
                            borderColor: '#fff',
                            bgcolor: alpha('#fff', 0.1),
                          },
                        }}
                      >
                        Learn More
                      </Button>
                    </Stack>
                  </Stack>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center',
                    }}
                  >
                    <AutoAwesome sx={{ fontSize: 120, opacity: 0.3 }} />
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
            {/* Background decoration */}
            <Box
              sx={{
                position: 'absolute',
                top: -100,
                right: -100,
                width: 300,
                height: 300,
                borderRadius: '50%',
                bgcolor: alpha('#fff', 0.1),
              }}
            />
          </Card>
        </Fade>
      )}
    </Box>
  )
}
