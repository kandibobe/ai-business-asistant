import { useState } from 'react'
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
  Divider,
  Alert,
} from '@mui/material'
import { Save } from '@mui/icons-material'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/store'
import {
  updateLanguage,
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

  const [saved, setSaved] = useState(false)

  const handleChange = (field: string, value: any) => {
    setLocalSettings({ ...localSettings, [field]: value })
    setSaved(false)
  }

  const handleSave = async () => {
    dispatch(saveSettingsStart())

    try {
      const updatedSettings = await settingsApi.update(localSettings)
      dispatch(saveSettingsSuccess(updatedSettings))
      setSaved(true)
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
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Settings
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Customize your AI assistant preferences
        </Typography>
      </Box>

      {saved && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSaved(false)}>
          Settings saved successfully!
        </Alert>
      )}

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" fontWeight={600} gutterBottom>
            Profile Information
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
          </Box>
        </CardContent>
      </Card>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" fontWeight={600} gutterBottom>
            AI Assistant Settings
          </Typography>
          <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', gap: 3 }}>
            <FormControl fullWidth>
              <InputLabel>Language</InputLabel>
              <Select
                value={localSettings.language}
                label="Language"
                onChange={(e) => handleChange('language', e.target.value)}
              >
                <MenuItem value="en">English</MenuItem>
                <MenuItem value="ru">Русский</MenuItem>
                <MenuItem value="uk">Українська</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>AI Role</InputLabel>
              <Select
                value={localSettings.ai_role}
                label="AI Role"
                onChange={(e) => handleChange('ai_role', e.target.value)}
              >
                <MenuItem value="assistant">Assistant</MenuItem>
                <MenuItem value="analyst">Analyst</MenuItem>
                <MenuItem value="consultant">Consultant</MenuItem>
                <MenuItem value="advisor">Advisor</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Response Style</InputLabel>
              <Select
                value={localSettings.response_style}
                label="Response Style"
                onChange={(e) => handleChange('response_style', e.target.value)}
              >
                <MenuItem value="concise">Concise</MenuItem>
                <MenuItem value="standard">Standard</MenuItem>
                <MenuItem value="detailed">Detailed</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>AI Mode</InputLabel>
              <Select
                value={localSettings.ai_mode}
                label="AI Mode"
                onChange={(e) => handleChange('ai_mode', e.target.value)}
              >
                <MenuItem value="standard">Standard</MenuItem>
                <MenuItem value="creative">Creative</MenuItem>
                <MenuItem value="analytical">Analytical</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </CardContent>
      </Card>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" fontWeight={600} gutterBottom>
            Notifications
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
              label="Enable notifications"
            />
          </Box>
        </CardContent>
      </Card>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<Save />}
          onClick={handleSave}
          disabled={settings.isSaving}
        >
          {settings.isSaving ? 'Saving...' : 'Save Changes'}
        </Button>
      </Box>
    </Box>
  )
}
