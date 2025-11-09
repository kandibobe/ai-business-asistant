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
} from '@mui/material'
import {
  Check,
  Star,
  Speed,
  CloudUpload,
  Analytics,
  Support,
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
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h3" fontWeight={700} gutterBottom>
          Upgrade to Premium
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Unlock the full potential of AI-powered business intelligence
        </Typography>
      </Box>

      <Grid container spacing={4} sx={{ mb: 6 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card sx={{ textAlign: 'center', height: '100%' }}>
              <CardContent>
                <Box sx={{ color: 'primary.main', mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} justifyContent="center">
        {plans.map((plan, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Card
              sx={{
                height: '100%',
                position: 'relative',
                border: plan.recommended ? 2 : 0,
                borderColor: 'primary.main',
              }}
            >
              {plan.recommended && (
                <Chip
                  label="RECOMMENDED"
                  color="primary"
                  icon={<Star />}
                  sx={{
                    position: 'absolute',
                    top: -12,
                    left: '50%',
                    transform: 'translateX(-50%)',
                  }}
                />
              )}
              <CardContent sx={{ textAlign: 'center', pt: 4 }}>
                <Typography variant="h5" fontWeight={700} gutterBottom>
                  {plan.name}
                </Typography>
                <Box sx={{ my: 3 }}>
                  <Typography variant="h3" fontWeight={700} component="span">
                    {plan.price}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {plan.period}
                  </Typography>
                </Box>
                <List sx={{ textAlign: 'left', mb: 3 }}>
                  {plan.features.map((feature, idx) => (
                    <ListItem key={idx} dense>
                      <ListItemIcon sx={{ minWidth: 36 }}>
                        <Check color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={feature}
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItem>
                  ))}
                </List>
                <Button
                  variant={plan.recommended ? 'contained' : 'outlined'}
                  fullWidth
                  size="large"
                  disabled={plan.current}
                >
                  {plan.current ? 'Current Plan' : 'Upgrade Now'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {!user?.is_premium && (
        <Card sx={{ mt: 6, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <CardContent sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h5" fontWeight={700} sx={{ color: 'white', mb: 2 }}>
              Try Premium Free for 14 Days
            </Typography>
            <Typography variant="body1" sx={{ color: 'white', mb: 3 }}>
              No credit card required. Cancel anytime.
            </Typography>
            <Button
              variant="contained"
              size="large"
              sx={{
                backgroundColor: 'white',
                color: '#667eea',
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.9)',
                },
              }}
            >
              Start Free Trial
            </Button>
          </CardContent>
        </Card>
      )}
    </Box>
  )
}
