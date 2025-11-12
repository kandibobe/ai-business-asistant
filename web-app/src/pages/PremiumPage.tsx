import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Fade,
  Zoom,
  Grow,
} from '@mui/material'
import {
  Check,
  Star,
  Speed,
  CloudUpload,
  Analytics,
  Support,
  AutoAwesome,
} from '@mui/icons-material'
import { useSelector } from 'react-redux'
import { RootState } from '@/store'

export default function PremiumPage() {
  const { user } = useSelector((state: RootState) => state.auth)

  const features = [
    {
      icon: <CloudUpload />,
      title: 'Unlimited Documents',
      description: 'Upload and process unlimited documents',
    },
    {
      icon: <Speed />,
      title: 'Priority Processing',
      description: '5x faster document processing and AI responses',
    },
    {
      icon: <Analytics />,
      title: 'Advanced Analytics',
      description: 'Access detailed insights and custom reports',
    },
    {
      icon: <Support />,
      title: 'Priority Support',
      description: '24/7 dedicated customer support',
    },
  ]

  const plans = [
    {
      name: 'Free',
      price: '$0',
      period: 'forever',
      features: [
        'Up to 5 documents',
        'Standard processing speed',
        'Basic analytics',
        'Email support',
      ],
      current: !user?.is_premium,
    },
    {
      name: 'Premium',
      price: '$29',
      period: 'per month',
      features: [
        'Unlimited documents',
        'Priority processing (5x faster)',
        'Advanced analytics & reports',
        '24/7 priority support',
        'API access',
        'Custom AI roles',
      ],
      current: user?.is_premium,
      recommended: true,
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: 'contact us',
      features: [
        'Everything in Premium',
        'Dedicated infrastructure',
        'Custom integrations',
        'Team collaboration',
        'SLA guarantee',
        'On-premise deployment',
      ],
      current: false,
    },
  ]

  return (
    <Box>
      <Zoom in={true} timeout={600}>
        <Box sx={{ textAlign: 'center', mb: 6, position: 'relative' }}>
          <AutoAwesome
            sx={{
              position: 'absolute',
              top: -20,
              left: '50%',
              transform: 'translateX(-50%)',
              fontSize: 48,
              color: 'warning.main',
              animation: 'pulse 2s ease-in-out infinite',
              '@keyframes pulse': {
                '0%, 100%': { opacity: 1, transform: 'translateX(-50%) scale(1)' },
                '50%': { opacity: 0.5, transform: 'translateX(-50%) scale(1.2)' },
              },
            }}
          />
          <Typography variant="h3" fontWeight={700} gutterBottom sx={{ mt: 2 }}>
            ✨ Upgrade to Premium
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Unlock the full potential of AI-powered business intelligence
          </Typography>
        </Box>
      </Zoom>

      <Grid container spacing={4} sx={{ mb: 6 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Grow in={true} timeout={800 + index * 200}>
              <Card
                sx={{
                  textAlign: 'center',
                  height: '100%',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'translateY(-12px) scale(1.05)',
                    boxShadow: 8,
                  },
                }}
              >
                <CardContent>
                  <Box
                    sx={{
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      borderRadius: '50%',
                      width: 64,
                      height: 64,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      margin: '0 auto 16px',
                      color: 'white',
                    }}
                  >
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" fontWeight={600} gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grow>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} justifyContent="center">
        {plans.map((plan, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Zoom in={true} timeout={1200 + index * 200}>
              <Card
                sx={{
                  height: '100%',
                  position: 'relative',
                  border: plan.recommended ? 3 : 0,
                  borderColor: plan.recommended ? 'primary.main' : undefined,
                  background: plan.recommended
                    ? 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)'
                    : undefined,
                  transition: 'all 0.4s ease',
                  '&:hover': {
                    transform: plan.recommended ? 'scale(1.08)' : 'scale(1.04)',
                    boxShadow: plan.recommended ? 12 : 8,
                  },
                }}
              >
                {plan.recommended && (
                  <Chip
                    label="⭐ RECOMMENDED"
                    color="primary"
                    sx={{
                      position: 'absolute',
                      top: -12,
                      left: '50%',
                      transform: 'translateX(-50%)',
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      color: 'white',
                      fontWeight: 700,
                      fontSize: '0.8rem',
                      animation: 'pulse 2s ease-in-out infinite',
                    }}
                  />
                )}
                <CardContent sx={{ textAlign: 'center', pt: 4 }}>
                  <Typography variant="h5" fontWeight={700} gutterBottom>
                    {plan.name}
                  </Typography>
                  <Box sx={{ my: 3 }}>
                    <Typography
                      variant="h3"
                      fontWeight={700}
                      component="span"
                      sx={{
                        background: plan.recommended
                          ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                          : undefined,
                        WebkitBackgroundClip: plan.recommended ? 'text' : undefined,
                        WebkitTextFillColor: plan.recommended ? 'transparent' : undefined,
                      }}
                    >
                      {plan.price}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {plan.period}
                    </Typography>
                  </Box>
                  <List sx={{ textAlign: 'left', mb: 3 }}>
                    {plan.features.map((feature, idx) => (
                      <Grow key={idx} in={true} timeout={1400 + index * 200 + idx * 100}>
                        <ListItem dense>
                          <ListItemIcon sx={{ minWidth: 36 }}>
                            <Check
                              sx={{
                                color: plan.recommended ? 'primary.main' : 'success.main',
                                fontWeight: 700,
                              }}
                            />
                          </ListItemIcon>
                          <ListItemText
                            primary={feature}
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItem>
                      </Grow>
                    ))}
                  </List>
                  <Button
                    variant={plan.recommended ? 'contained' : 'outlined'}
                    fullWidth
                    size="large"
                    disabled={plan.current}
                    sx={{
                      background: plan.recommended && !plan.current
                        ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                        : undefined,
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        transform: !plan.current ? 'scale(1.05)' : undefined,
                        boxShadow: !plan.current ? 4 : undefined,
                      },
                    }}
                  >
                    {plan.current ? '✅ Current Plan' : '🚀 Upgrade Now'}
                  </Button>
                </CardContent>
              </Card>
            </Zoom>
          </Grid>
        ))}
      </Grid>

      {!user?.is_premium && (
        <Fade in={true} timeout={2000}>
          <Card
            sx={{
              mt: 6,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              position: 'relative',
              overflow: 'hidden',
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'translateY(-8px)',
                boxShadow: 12,
              },
              '&::before': {
                content: '""',
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'radial-gradient(circle at 30% 50%, rgba(255,255,255,0.15), transparent)',
              },
            }}
          >
            <CardContent sx={{ textAlign: 'center', py: 6, position: 'relative' }}>
              <Typography variant="h4" fontWeight={700} sx={{ color: 'white', mb: 2 }}>
                🎉 Try Premium Free for 14 Days
              </Typography>
              <Typography variant="h6" sx={{ color: 'white', mb: 4, opacity: 0.95 }}>
                No credit card required. Cancel anytime.
              </Typography>
              <Button
                variant="contained"
                size="large"
                sx={{
                  backgroundColor: 'white',
                  color: '#667eea',
                  fontWeight: 700,
                  px: 5,
                  py: 2,
                  fontSize: '1.1rem',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    backgroundColor: 'rgba(255,255,255,0.95)',
                    transform: 'scale(1.1)',
                    boxShadow: 8,
                  },
                }}
              >
                ✨ Start Free Trial
              </Button>
            </CardContent>
          </Card>
        </Fade>
      )}
    </Box>
  )
}
