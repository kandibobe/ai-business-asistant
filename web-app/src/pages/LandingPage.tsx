import { useNavigate } from 'react-router-dom'
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  useTheme,
  alpha,
  Stack,
  Chip,
} from '@mui/material'
import {
  SmartToy,
  Description,
  Analytics,
  Speed,
  Security,
  CloudUpload,
  Star,
  ArrowForward,
  CheckCircle,
} from '@mui/icons-material'

const features = [
  {
    icon: <SmartToy sx={{ fontSize: 40 }} />,
    title: 'AI-Powered Assistant',
    description: 'Get instant answers powered by advanced Google Gemini AI technology',
  },
  {
    icon: <Description sx={{ fontSize: 40 }} />,
    title: 'Document Analysis',
    description: 'Upload and analyze documents with intelligent text extraction',
  },
  {
    icon: <Analytics sx={{ fontSize: 40 }} />,
    title: 'Advanced Analytics',
    description: 'Track your usage, questions, and get detailed insights',
  },
  {
    icon: <Speed sx={{ fontSize: 40 }} />,
    title: 'Lightning Fast',
    description: 'Optimized performance with intelligent caching for instant responses',
  },
  {
    icon: <Security sx={{ fontSize: 40 }} />,
    title: 'Secure & Private',
    description: 'Enterprise-grade security with encrypted data storage',
  },
  {
    icon: <CloudUpload sx={{ fontSize: 40 }} />,
    title: 'Cloud Storage',
    description: 'Store and access your documents and chat history from anywhere',
  },
]

const plans = [
  {
    name: 'Free',
    price: '$0',
    period: '/month',
    features: [
      '100 AI messages per month',
      '5 document uploads',
      'Basic analytics',
      'Email support',
    ],
    popular: false,
  },
  {
    name: 'Premium',
    price: '$19',
    period: '/month',
    features: [
      'Unlimited AI messages',
      'Unlimited document uploads',
      'Advanced analytics',
      'Priority support',
      'Custom integrations',
      'API access',
    ],
    popular: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    period: '',
    features: [
      'Everything in Premium',
      'Dedicated support',
      'Custom AI models',
      'SLA guarantee',
      'On-premise deployment',
      'Custom training',
    ],
    popular: false,
  },
]

export default function LandingPage() {
  const navigate = useNavigate()
  const theme = useTheme()

  return (
    <Box>
      {/* Header */}
      <Box
        sx={{
          position: 'sticky',
          top: 0,
          zIndex: 1000,
          bgcolor: alpha(theme.palette.background.paper, 0.8),
          backdropFilter: 'blur(10px)',
          borderBottom: `1px solid ${theme.palette.divider}`,
        }}
      >
        <Container maxWidth="lg">
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              py: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <SmartToy sx={{ fontSize: 32, color: 'primary.main' }} />
              <Typography variant="h6" fontWeight={700}>
                AI Business Assistant
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button variant="outlined" onClick={() => navigate('/login')}>
                Sign In
              </Button>
              <Button
                variant="contained"
                onClick={() => navigate('/login')}
                endIcon={<ArrowForward />}
              >
                Get Started
              </Button>
            </Box>
          </Box>
        </Container>
      </Box>

      {/* Hero Section */}
      <Box
        sx={{
          background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
          color: 'white',
          pt: 12,
          pb: 16,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Stack spacing={3}>
                <Chip
                  label="Powered by Google Gemini AI"
                  icon={<Star />}
                  sx={{
                    alignSelf: 'flex-start',
                    bgcolor: alpha('#fff', 0.2),
                    color: 'white',
                    fontWeight: 600,
                  }}
                />
                <Typography
                  variant="h2"
                  fontWeight={800}
                  sx={{
                    fontSize: { xs: '2.5rem', md: '3.5rem' },
                    lineHeight: 1.2,
                  }}
                >
                  Your Intelligent Business Assistant
                </Typography>
                <Typography
                  variant="h5"
                  sx={{
                    opacity: 0.95,
                    fontWeight: 400,
                    fontSize: { xs: '1.2rem', md: '1.5rem' },
                  }}
                >
                  Streamline your workflow with AI-powered document analysis,
                  intelligent chat, and powerful analytics
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={() => navigate('/login')}
                    sx={{
                      bgcolor: 'white',
                      color: 'primary.main',
                      px: 4,
                      py: 1.5,
                      fontSize: '1.1rem',
                      fontWeight: 600,
                      '&:hover': {
                        bgcolor: alpha('#fff', 0.9),
                      },
                    }}
                    endIcon={<ArrowForward />}
                  >
                    Start Free Trial
                  </Button>
                  <Button
                    variant="outlined"
                    size="large"
                    sx={{
                      borderColor: 'white',
                      color: 'white',
                      px: 4,
                      py: 1.5,
                      fontSize: '1.1rem',
                      fontWeight: 600,
                      '&:hover': {
                        borderColor: 'white',
                        bgcolor: alpha('#fff', 0.1),
                      },
                    }}
                  >
                    Watch Demo
                  </Button>
                </Box>
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  position: 'relative',
                  height: { xs: 300, md: 400 },
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Box
                  sx={{
                    width: 300,
                    height: 300,
                    borderRadius: '50%',
                    bgcolor: alpha('#fff', 0.1),
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    animation: 'pulse 3s ease-in-out infinite',
                    '@keyframes pulse': {
                      '0%, 100%': { transform: 'scale(1)' },
                      '50%': { transform: 'scale(1.05)' },
                    },
                  }}
                >
                  <SmartToy sx={{ fontSize: 150, opacity: 0.9 }} />
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 12 }}>
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography
            variant="h3"
            fontWeight={700}
            gutterBottom
            sx={{ fontSize: { xs: '2rem', md: '3rem' } }}
          >
            Powerful Features
          </Typography>
          <Typography
            variant="h6"
            color="text.secondary"
            sx={{ maxWidth: 600, mx: 'auto' }}
          >
            Everything you need to boost your productivity and streamline your
            business operations
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                sx={{
                  height: '100%',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: theme.shadows[10],
                  },
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Box
                    sx={{
                      color: 'primary.main',
                      mb: 2,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      width: 70,
                      height: 70,
                      borderRadius: 2,
                      bgcolor: alpha(theme.palette.primary.main, 0.1),
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
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Pricing Section */}
      <Box sx={{ bgcolor: 'background.default', py: 12 }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', mb: 8 }}>
            <Typography
              variant="h3"
              fontWeight={700}
              gutterBottom
              sx={{ fontSize: { xs: '2rem', md: '3rem' } }}
            >
              Simple, Transparent Pricing
            </Typography>
            <Typography variant="h6" color="text.secondary">
              Choose the perfect plan for your needs
            </Typography>
          </Box>

          <Grid container spacing={4} justifyContent="center">
            {plans.map((plan, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card
                  sx={{
                    height: '100%',
                    position: 'relative',
                    border: plan.popular
                      ? `2px solid ${theme.palette.primary.main}`
                      : 'none',
                    transform: plan.popular ? 'scale(1.05)' : 'none',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: plan.popular ? 'scale(1.08)' : 'scale(1.03)',
                      boxShadow: theme.shadows[10],
                    },
                  }}
                >
                  {plan.popular && (
                    <Chip
                      label="Most Popular"
                      color="primary"
                      sx={{
                        position: 'absolute',
                        top: 16,
                        right: 16,
                        fontWeight: 600,
                      }}
                    />
                  )}
                  <CardContent sx={{ p: 4 }}>
                    <Typography variant="h5" fontWeight={700} gutterBottom>
                      {plan.name}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'baseline', mb: 3 }}>
                      <Typography variant="h3" fontWeight={800}>
                        {plan.price}
                      </Typography>
                      <Typography variant="body1" color="text.secondary">
                        {plan.period}
                      </Typography>
                    </Box>
                    <Stack spacing={2} sx={{ mb: 4 }}>
                      {plan.features.map((feature, idx) => (
                        <Box
                          key={idx}
                          sx={{ display: 'flex', alignItems: 'center', gap: 1 }}
                        >
                          <CheckCircle
                            sx={{ color: 'success.main', fontSize: 20 }}
                          />
                          <Typography variant="body2">{feature}</Typography>
                        </Box>
                      ))}
                    </Stack>
                    <Button
                      variant={plan.popular ? 'contained' : 'outlined'}
                      fullWidth
                      size="large"
                      onClick={() => navigate('/login')}
                    >
                      {plan.price === 'Custom' ? 'Contact Sales' : 'Get Started'}
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box
        sx={{
          background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
          color: 'white',
          py: 10,
        }}
      >
        <Container maxWidth="md">
          <Box sx={{ textAlign: 'center' }}>
            <Typography
              variant="h3"
              fontWeight={700}
              gutterBottom
              sx={{ fontSize: { xs: '2rem', md: '3rem' } }}
            >
              Ready to Get Started?
            </Typography>
            <Typography
              variant="h6"
              sx={{ mb: 4, opacity: 0.95, fontWeight: 400 }}
            >
              Join thousands of businesses already using our AI assistant to
              streamline their operations
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/login')}
              sx={{
                bgcolor: 'white',
                color: 'primary.main',
                px: 6,
                py: 2,
                fontSize: '1.2rem',
                fontWeight: 600,
                '&:hover': {
                  bgcolor: alpha('#fff', 0.9),
                },
              }}
              endIcon={<ArrowForward />}
            >
              Start Your Free Trial
            </Button>
          </Box>
        </Container>
      </Box>

      {/* Footer */}
      <Box sx={{ bgcolor: 'background.paper', py: 6, borderTop: `1px solid ${theme.palette.divider}` }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <SmartToy sx={{ fontSize: 28, color: 'primary.main' }} />
                <Typography variant="h6" fontWeight={700}>
                  AI Business Assistant
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Empowering businesses with intelligent AI solutions for better
                productivity and insights.
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4} md={2}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Product
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary">
                  Features
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Pricing
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Security
                </Typography>
              </Stack>
            </Grid>
            <Grid item xs={12} sm={4} md={2}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Company
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary">
                  About
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Blog
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Careers
                </Typography>
              </Stack>
            </Grid>
            <Grid item xs={12} sm={4} md={2}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Support
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary">
                  Help Center
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Contact
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Status
                </Typography>
              </Stack>
            </Grid>
            <Grid item xs={12} sm={4} md={2}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Legal
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary">
                  Privacy
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Terms
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Cookie Policy
                </Typography>
              </Stack>
            </Grid>
          </Grid>
          <Box sx={{ mt: 6, pt: 3, borderTop: `1px solid ${theme.palette.divider}`, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              © 2024 AI Business Assistant. All rights reserved.
            </Typography>
          </Box>
        </Container>
      </Box>
    </Box>
  )
}
