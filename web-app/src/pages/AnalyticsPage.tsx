import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
} from '@mui/material'
import {
  BarChart,
  Timeline,
  PieChart,
} from '@mui/icons-material'

export default function AnalyticsPage() {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Analytics
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Track your usage patterns and AI performance metrics
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <BarChart sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Usage Statistics
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Coming soon
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <Timeline sx={{ fontSize: 60, color: 'secondary.main', mb: 2 }} />
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Response Time Trends
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Coming soon
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <PieChart sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Document Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Coming soon
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" fontWeight={600} gutterBottom>
            Advanced Analytics
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Detailed charts and visualizations will be available here, including:
          </Typography>
          <Box component="ul" sx={{ mt: 2 }}>
            <li>
              <Typography variant="body2">Question frequency over time</Typography>
            </li>
            <li>
              <Typography variant="body2">Document processing metrics</Typography>
            </li>
            <li>
              <Typography variant="body2">AI response quality ratings</Typography>
            </li>
            <li>
              <Typography variant="body2">Most queried topics</Typography>
            </li>
          </Box>
        </CardContent>
      </Card>
    </Box>
  )
}
