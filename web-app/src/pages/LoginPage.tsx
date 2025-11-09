import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Link,
  Alert,
  InputAdornment,
  IconButton,
  Divider,
} from '@mui/material'
import {
  Visibility,
  VisibilityOff,
  AccountCircle,
  Lock,
} from '@mui/icons-material'
import { useDispatch } from 'react-redux'
import { loginStart, loginSuccess, loginFailure } from '@/store/slices/authSlice'
import apiClient from '@/api/client'

export default function LoginPage() {
  const navigate = useNavigate()
  const dispatch = useDispatch()

  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    first_name: '',
  })
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
    setError(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    dispatch(loginStart())

    try {
      if (isLogin) {
        // Login
        const response = await apiClient.post('/auth/login', {
          username: formData.username,
          password: formData.password,
        })

        dispatch(loginSuccess(response.data))
        navigate('/dashboard')
      } else {
        // Register
        const response = await apiClient.post('/auth/register', {
          username: formData.username,
          password: formData.password,
          email: formData.email,
          first_name: formData.first_name,
        })

        dispatch(loginSuccess(response.data))
        navigate('/dashboard')
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Authentication failed'
      setError(errorMessage)
      dispatch(loginFailure(errorMessage))
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: 2,
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={10}
          sx={{
            p: 4,
            borderRadius: 2,
          }}
        >
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              AI Business Assistant
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {isLogin ? 'Sign in to your account' : 'Create a new account'}
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              margin="normal"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <AccountCircle />
                  </InputAdornment>
                ),
              }}
            />

            {!isLogin && (
              <>
                <TextField
                  fullWidth
                  label="Email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="First Name"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  margin="normal"
                />
              </>
            )}

            <TextField
              fullWidth
              label="Password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={handleChange}
              required
              margin="normal"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Lock />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{ mt: 3, mb: 2 }}
            >
              {loading ? 'Please wait...' : isLogin ? 'Sign In' : 'Sign Up'}
            </Button>

            <Divider sx={{ my: 2 }} />

            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2">
                {isLogin ? "Don't have an account? " : 'Already have an account? '}
                <Link
                  component="button"
                  type="button"
                  onClick={() => {
                    setIsLogin(!isLogin)
                    setError(null)
                    setFormData({ username: '', password: '', email: '', first_name: '' })
                  }}
                  sx={{ textDecoration: 'none', fontWeight: 600 }}
                >
                  {isLogin ? 'Sign Up' : 'Sign In'}
                </Link>
              </Typography>
            </Box>
          </form>
        </Paper>
      </Container>
    </Box>
  )
}
