import React from 'react'
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Stack,
  Chip,
  useTheme,
  alpha,
} from '@mui/material'
import { useNavigate } from 'react-router-dom'
import {
  AutoAwesome,
  Description,
  Speed,
  Security,
  Analytics,
  CloudUpload,
  Chat,
  TrendingUp,
  CheckCircle,
} from '@mui/icons-material'
import { gradients } from '../theme'

const LandingPage: React.FC = () => {
  const navigate = useNavigate()
  const theme = useTheme()

  const features = [
    {
      icon: <AutoAwesome sx={{ fontSize: 40 }} />,
      title: 'AI-Powered Intelligence',
      description: 'Advanced AI algorithms analyze your documents and provide intelligent insights instantly.',
      color: gradients.primary,
    },
    {
      icon: <Description sx={{ fontSize: 40 }} />,
      title: 'Document Management',
      description: 'Upload, organize, and process multiple document types including PDF, Excel, and Word files.',
      color: gradients.success,
    },
    {
      icon: <Chat sx={{ fontSize: 40 }} />,
      title: 'Smart Chat',
      description: 'Have natural conversations with AI about your documents and get instant answers.',
      color: gradients.info,
    },
    {
      icon: <Analytics sx={{ fontSize: 40 }} />,
      title: 'Advanced Analytics',
      description: 'Get detailed insights and analytics about your documents and usage patterns.',
      color: gradients.warning,
    },
    {
      icon: <Speed sx={{ fontSize: 40 }} />,
      title: 'Lightning Fast',
      description: 'Process documents in seconds with our optimized AI pipeline.',
      color: gradients.secondary,
    },
    {
      icon: <Security sx={{ fontSize: 40 }} />,
      title: 'Secure & Private',
      description: 'Your data is encrypted and secure. We prioritize your privacy and data protection.',
      color: gradients.royal,
    },
  ]

  const howItWorks = [
    {
      step: '1',
      title: 'Upload Documents',
      description: 'Simply drag and drop your documents or upload them through our interface.',
      icon: <CloudUpload sx={{ fontSize: 48 }} />,
    },
    {
      step: '2',
      title: 'AI Processing',
      description: 'Our AI analyzes your documents, extracts key information and generates insights.',
      icon: <AutoAwesome sx={{ fontSize: 48 }} />,
    },
    {
      step: '3',
      title: 'Get Insights',
      description: 'Chat with AI about your documents, get analytics, and make data-driven decisions.',
      icon: <TrendingUp sx={{ fontSize: 48 }} />,
    },
  ]

  const benefits = [
    'Unlimited document uploads',
    'Advanced AI chat capabilities',
    'Real-time document processing',
    'Detailed analytics and reports',
    'Multi-language support',
    'Secure cloud storage',
    'Export functionality',
    '24/7 customer support',
  ]

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Header */}
      <Box
        component="header"
        sx={{
          position: 'sticky',
          top: 0,
          zIndex: 1000,
          backdropFilter: 'blur(10px)',
          backgroundColor: alpha(theme.palette.background.paper, 0.8),
          borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
        }}
      >
        <Container maxWidth="lg">
          <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="center"
            py={2}
          >
            <Typography variant="h5" fontWeight={700} sx={{
              background: gradients.primary,
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>
              AI Business Assistant
            </Typography>
            <Stack direction="row" spacing={2}>
              <Button
                variant="outlined"
                onClick={() => navigate('/login')}
                sx={{ borderRadius: 2 }}
              >
                Sign In
              </Button>
              <Button
                variant="contained"
                onClick={() => navigate('/login')}
                sx={{ borderRadius: 2 }}
              >
                Get Started
              </Button>
            </Stack>
          </Stack>
        </Container>
      </Box>

      {/* Hero Section */}
      <Box
        sx={{
          position: 'relative',
          overflow: 'hidden',
          pt: { xs: 8, md: 12 },
          pb: { xs: 8, md: 12 },
          background: gradients.primary,
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Stack spacing={3}>
                <Chip
                  label="✨ AI-Powered Platform"
                  sx={{
                    width: 'fit-content',
                    bgcolor: alpha('#fff', 0.2),
                    color: '#fff',
                    fontWeight: 600,
                  }}
                />
                <Typography
                  variant="h1"
                  sx={{
                    fontSize: { xs: '2.5rem', md: '3.5rem' },
                    fontWeight: 800,
                    color: '#fff',
                    lineHeight: 1.1,
                  }}
                >
                  Transform Your Documents with AI
                </Typography>
                <Typography
                  variant="h5"
                  sx={{
                    color: alpha('#fff', 0.9),
                    fontWeight: 400,
                    lineHeight: 1.6,
                  }}
                >
                  Upload, analyze, and chat with your documents using advanced AI.
                  Get instant insights and make smarter business decisions.
                </Typography>
                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} pt={2}>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={() => navigate('/login')}
                    sx={{
                      bgcolor: '#fff',
                      color: theme.palette.primary.main,
                      '&:hover': {
                        bgcolor: alpha('#fff', 0.9),
                      },
                      fontSize: '1.125rem',
                      py: 1.5,
                      px: 4,
                    }}
                  >
                    Start Free Trial
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
                      fontSize: '1.125rem',
                      py: 1.5,
                      px: 4,
                    }}
                  >
                    Watch Demo
                  </Button>
                </Stack>
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  position: 'relative',
                  width: '100%',
                  height: { xs: 300, md: 400 },
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Box
                  sx={{
                    width: '80%',
                    height: '80%',
                    borderRadius: 4,
                    bgcolor: alpha('#fff', 0.1),
                    backdropFilter: 'blur(10px)',
                    border: `2px solid ${alpha('#fff', 0.2)}`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <AutoAwesome sx={{ fontSize: 120, color: '#fff', opacity: 0.5 }} />
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: { xs: 8, md: 12 } }}>
        <Stack spacing={6}>
          <Box textAlign="center">
            <Typography variant="h2" gutterBottom fontWeight={700}>
              Powerful Features
            </Typography>
            <Typography variant="h6" color="text.secondary" maxWidth="md" mx="auto">
              Everything you need to manage and analyze your documents with AI
            </Typography>
          </Box>

          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card
                  sx={{
                    height: '100%',
                    transition: 'all 0.3s',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                    },
                  }}
                >
                  <CardContent sx={{ p: 4 }}>
                    <Stack spacing={2}>
                      <Box
                        sx={{
                          width: 64,
                          height: 64,
                          borderRadius: 3,
                          background: feature.color,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: '#fff',
                        }}
                      >
                        {feature.icon}
                      </Box>
                      <Typography variant="h5" fontWeight={600}>
                        {feature.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" lineHeight={1.7}>
                        {feature.description}
                      </Typography>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Stack>
      </Container>

      {/* How It Works Section */}
      <Box sx={{ bgcolor: 'background.paper', py: { xs: 8, md: 12 } }}>
        <Container maxWidth="lg">
          <Stack spacing={6}>
            <Box textAlign="center">
              <Typography variant="h2" gutterBottom fontWeight={700}>
                How It Works
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Get started in three simple steps
              </Typography>
            </Box>

            <Grid container spacing={4}>
              {howItWorks.map((item, index) => (
                <Grid item xs={12} md={4} key={index}>
                  <Card
                    sx={{
                      height: '100%',
                      textAlign: 'center',
                      position: 'relative',
                    }}
                  >
                    <CardContent sx={{ p: 4 }}>
                      <Stack spacing={2} alignItems="center">
                        <Box
                          sx={{
                            width: 80,
                            height: 80,
                            borderRadius: '50%',
                            background: gradients.primary,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: '#fff',
                            mb: 2,
                          }}
                        >
                          {item.icon}
                        </Box>
                        <Chip
                          label={`Step ${item.step}`}
                          sx={{
                            bgcolor: theme.palette.primary.main,
                            color: '#fff',
                            fontWeight: 600,
                          }}
                        />
                        <Typography variant="h5" fontWeight={600}>
                          {item.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" lineHeight={1.7}>
                          {item.description}
                        </Typography>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Stack>
        </Container>
      </Box>

      {/* Benefits Section */}
      <Container maxWidth="lg" sx={{ py: { xs: 8, md: 12 } }}>
        <Grid container spacing={6} alignItems="center">
          <Grid item xs={12} md={6}>
            <Stack spacing={3}>
              <Typography variant="h2" fontWeight={700}>
                Why Choose Us?
              </Typography>
              <Typography variant="h6" color="text.secondary" lineHeight={1.7}>
                Join thousands of businesses that trust our AI-powered platform
                to manage and analyze their documents efficiently.
              </Typography>
              <Grid container spacing={2}>
                {benefits.map((benefit, index) => (
                  <Grid item xs={12} sm={6} key={index}>
                    <Stack direction="row" spacing={1} alignItems="center">
                      <CheckCircle color="success" />
                      <Typography variant="body1">{benefit}</Typography>
                    </Stack>
                  </Grid>
                ))}
              </Grid>
              <Box pt={2}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/login')}
                  sx={{ py: 1.5, px: 4 }}
                >
                  Get Started Now
                </Button>
              </Box>
            </Stack>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                width: '100%',
                height: 400,
                borderRadius: 4,
                background: gradients.success,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Typography variant="h3" color="#fff" fontWeight={700}>
                Visual Placeholder
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box
        sx={{
          background: gradients.royal,
          py: { xs: 8, md: 10 },
        }}
      >
        <Container maxWidth="md">
          <Stack spacing={4} alignItems="center" textAlign="center">
            <Typography
              variant="h2"
              fontWeight={700}
              color="#fff"
              sx={{ fontSize: { xs: '2rem', md: '2.5rem' } }}
            >
              Ready to Transform Your Workflow?
            </Typography>
            <Typography variant="h6" color={alpha('#fff', 0.9)} maxWidth="sm">
              Join thousands of businesses already using AI to streamline their document management.
            </Typography>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/login')}
                sx={{
                  bgcolor: '#fff',
                  color: theme.palette.primary.main,
                  '&:hover': {
                    bgcolor: alpha('#fff', 0.9),
                  },
                  fontSize: '1.125rem',
                  py: 1.5,
                  px: 4,
                }}
              >
                Start Free Trial
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
                  fontSize: '1.125rem',
                  py: 1.5,
                  px: 4,
                }}
              >
                Contact Sales
              </Button>
            </Stack>
          </Stack>
        </Container>
      </Box>

      {/* Footer */}
      <Box
        component="footer"
        sx={{
          bgcolor: 'background.paper',
          py: 6,
          borderTop: `1px solid ${theme.palette.divider}`,
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" fontWeight={700} gutterBottom sx={{
                background: gradients.primary,
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}>
                AI Business Assistant
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Transform your documents with the power of AI. Analyze, chat, and get insights instantly.
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4} md={2}>
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                Product
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Features
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Pricing
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Security
                </Typography>
              </Stack>
            </Grid>
            <Grid item xs={12} sm={4} md={2}>
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                Company
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  About
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Blog
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Careers
                </Typography>
              </Stack>
            </Grid>
            <Grid item xs={12} sm={4} md={2}>
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                Resources
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Documentation
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Help Center
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Contact
                </Typography>
              </Stack>
            </Grid>
            <Grid item xs={12} sm={4} md={2}>
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                Legal
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Privacy
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Terms
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ cursor: 'pointer' }}>
                  Cookie Policy
                </Typography>
              </Stack>
            </Grid>
          </Grid>
          <Box mt={6} pt={3} borderTop={`1px solid ${theme.palette.divider}`}>
            <Typography variant="body2" color="text.secondary" textAlign="center">
              © {new Date().getFullYear()} AI Business Assistant. All rights reserved.
            </Typography>
          </Box>
        </Container>
      </Box>
    </Box>
  )
}

export default LandingPage
