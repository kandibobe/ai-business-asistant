import { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Alert,
  Snackbar,
  Fade,
  Zoom,
} from '@mui/material'
import { Save } from '@mui/icons-material'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/store'
import {
  loadSettingsStart,
  loadSettingsSuccess,
  saveSettingsStart,
  saveSettingsSuccess,
  saveSettingsFailure,
} from '@/store/slices/settingsSlice'
import { showSnackbar } from '@/store/slices/uiSlice'
import { settingsApi } from '@/api/services'

export default function SettingsPage() {
  const dispatch = useDispatch()
  const settings = useSelector((state: RootState) => state.settings)
  const { user } = useSelector((state: RootState) => state.auth)

  const [localSettings, setLocalSettings] = useState({
    language: settings.language,
    ai_role: settings.ai_role,
    response_style: settings.response_style,
    ai_mode: settings.ai_mode,
    notifications_enabled: settings.notifications_enabled,
  })

  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({
    open: false,
    message: '',
    severity: 'info',
  })

  const [hasChanges, setHasChanges] = useState(false)

  // Load settings on mount
  useEffect(() => {
    loadSettings()
  }, [])

  // Update local settings when Redux store changes
  useEffect(() => {
    setLocalSettings({
      language: settings.language,
      ai_role: settings.ai_role,
      response_style: settings.response_style,
      ai_mode: settings.ai_mode,
      notifications_enabled: settings.notifications_enabled,
    })
  }, [settings])

  const loadSettings = async () => {
    try {
      dispatch(loadSettingsStart())
      const response = await settingsApi.get()
      dispatch(loadSettingsSuccess(response))
    } catch (error: any) {
      console.error('Failed to load settings:', error)
      dispatch(
        showSnackbar({
          message: 'Failed to load settings',
          severity: 'error',
        })
      )
    }
  }

  const handleChange = (field: string, value: any) => {
    setLocalSettings({ ...localSettings, [field]: value })
    setHasChanges(true)
  }

  const handleSave = async () => {
    dispatch(saveSettingsStart())

    try {
      const updatedSettings = await settingsApi.update(localSettings)
      dispatch(saveSettingsSuccess(updatedSettings))
      setHasChanges(false)
      dispatch(
        showSnackbar({
          message: 'Settings saved successfully!',
          severity: 'success',
        })
      )
    } catch (error: any) {
      dispatch(saveSettingsFailure(error.message))
      dispatch(
        showSnackbar({
          message: `Failed to save settings: ${error.message}`,
          severity: 'error',
        })
      )
    }
  }

  return (
    <Box>
      <Fade in={true} timeout={600}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            ⚙️ Settings
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Customize your AI assistant preferences
          </Typography>
        </Box>
      </Fade>

      {settings.error && (
        <Fade in={true} timeout={400}>
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => dispatch(saveSettingsFailure(''))}>
            {settings.error}
          </Alert>
        </Fade>
      )}

      <Zoom in={true} timeout={800}>
        <Card
          sx={{
            mb: 3,
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: 6,
            },
          }}
        >
          <CardContent>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              👤 Profile Information
            </Typography>
            <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', gap: 2 }}>
              <TextField
                label="Username"
                value={user?.username || ''}
                disabled
                fullWidth
              />
              <TextField
                label="First Name"
                value={user?.first_name || ''}
                disabled
                fullWidth
              />
              <TextField
                label="User ID"
                value={user?.user_id || ''}
                disabled
                fullWidth
              />
              {user?.is_premium && (
                <Fade in={true} timeout={1000}>
                  <Alert severity="success" sx={{ background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)', color: 'white' }}>
                    <strong>👑 Premium Member</strong>
                  </Alert>
                </Fade>
              )}
            </Box>
          </CardContent>
        </Card>
      </Zoom>

      <Zoom in={true} timeout={1000}>
        <Card
          sx={{
            mb: 3,
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: 6,
            },
          }}
        >
          <CardContent>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              🤖 AI Assistant Settings
            </Typography>
          <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', gap: 3 }}>
            <FormControl fullWidth>
              <InputLabel>Language</InputLabel>
              <Select
                value={localSettings.language}
                label="Language"
                onChange={(e) => handleChange('language', e.target.value)}
              >
                <MenuItem value="en">English 🇬🇧</MenuItem>
                <MenuItem value="ru">Русский 🇷🇺</MenuItem>
                <MenuItem value="de">Deutsch 🇩🇪</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>AI Role</InputLabel>
              <Select
                value={localSettings.ai_role}
                label="AI Role"
                onChange={(e) => handleChange('ai_role', e.target.value)}
              >
                <MenuItem value="assistant">Assistant - General help</MenuItem>
                <MenuItem value="analyst">Analyst - Data analysis</MenuItem>
                <MenuItem value="consultant">Consultant - Business advice</MenuItem>
                <MenuItem value="advisor">Advisor - Strategic guidance</MenuItem>
                <MenuItem value="teacher">Teacher - Educational focus</MenuItem>
                <MenuItem value="researcher">Researcher - Deep analysis</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Response Style</InputLabel>
              <Select
                value={localSettings.response_style}
                label="Response Style"
                onChange={(e) => handleChange('response_style', e.target.value)}
              >
                <MenuItem value="brief">Brief - Short answers</MenuItem>
                <MenuItem value="standard">Standard - Balanced</MenuItem>
                <MenuItem value="detailed">Detailed - Comprehensive</MenuItem>
                <MenuItem value="creative">Creative - Innovative</MenuItem>
                <MenuItem value="formal">Formal - Professional</MenuItem>
                <MenuItem value="casual">Casual - Friendly</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>AI Mode</InputLabel>
              <Select
                value={localSettings.ai_mode}
                label="AI Mode"
                onChange={(e) => handleChange('ai_mode', e.target.value)}
              >
                <MenuItem value="fast">Fast - Quick responses</MenuItem>
                <MenuItem value="standard">Standard - Balanced</MenuItem>
                <MenuItem value="advanced">Advanced - Deep analysis</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </CardContent>
      </Card>

      <Zoom in={true} timeout={1200}>
        <Card
          sx={{
            mb: 3,
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: 6,
            },
          }}
        >
          <CardContent>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              🔔 Notifications
            </Typography>
            <Box sx={{ mt: 2 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={localSettings.notifications_enabled}
                    onChange={(e) =>
                      handleChange('notifications_enabled', e.target.checked)
                    }
                  />
                }
                label="Enable notifications for document processing and AI responses"
              />
            </Box>
          </CardContent>
        </Card>
      </Zoom>

      <Fade in={true} timeout={1400}>
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
          <Button
            variant="outlined"
            size="large"
            onClick={() => {
              setLocalSettings({
                language: settings.language,
                ai_role: settings.ai_role,
                response_style: settings.response_style,
                ai_mode: settings.ai_mode,
                notifications_enabled: settings.notifications_enabled,
              })
              setHasChanges(false)
            }}
            disabled={!hasChanges || settings.isSaving}
            sx={{
              transition: 'all 0.2s ease',
              '&:hover': {
                transform: 'scale(1.05)',
              },
            }}
          >
            Reset
          </Button>
          <Button
            variant="contained"
            size="large"
            startIcon={<Save />}
            onClick={handleSave}
            disabled={!hasChanges || settings.isSaving}
            sx={{
              background: hasChanges ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : undefined,
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'scale(1.05)',
                boxShadow: 4,
              },
            }}
          >
            {settings.isSaving ? 'Saving...' : '💾 Save Changes'}
          </Button>
        </Box>
      </Fade>

      {/* Notification Snackbar */}
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={() => setNotification({ ...notification, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={() => setNotification({ ...notification, open: false })}
          severity={notification.severity}
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Box>
  )
}
