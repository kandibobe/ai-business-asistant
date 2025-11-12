import { Grid, Paper, Typography, Box, Chip, useTheme } from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Description as DocumentIcon,
  QuestionAnswer as QuestionIcon,
  Speed as SpeedIcon,
} from '@mui/icons-material';

interface StatCardProps {
  title: string;
  value: string | number;
  change?: number;
  icon: React.ReactNode;
  color: string;
  subtitle?: string;
}

function StatCard({ title, value, change, icon, color, subtitle }: StatCardProps) {
  const theme = useTheme();

  return (
    <Paper
      sx={{
        p: 3,
        height: '100%',
        position: 'relative',
        overflow: 'hidden',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: theme.shadows[8],
        },
      }}
    >
      {/* Background Icon */}
      <Box
        sx={{
          position: 'absolute',
          right: -10,
          top: -10,
          opacity: 0.1,
          transform: 'rotate(-15deg)',
          fontSize: '120px',
          color: color,
        }}
      >
        {icon}
      </Box>

      {/* Content */}
      <Box sx={{ position: 'relative', zIndex: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              width: 48,
              height: 48,
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              bgcolor: `${color}15`,
              color: color,
              mr: 2,
            }}
          >
            {icon}
          </Box>
          <Box>
            <Typography variant="body2" color="text.secondary">
              {title}
            </Typography>
            {change !== undefined && (
              <Chip
                label={`${change > 0 ? '+' : ''}${change}%`}
                size="small"
                sx={{
                  height: 20,
                  mt: 0.5,
                  bgcolor: change > 0 ? '#4caf5015' : '#f4433615',
                  color: change > 0 ? '#4caf50' : '#f44336',
                  fontSize: '0.7rem',
                  fontWeight: 600,
                }}
                icon={<TrendingUpIcon sx={{ fontSize: 14 }} />}
              />
            )}
          </Box>
        </Box>

        <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5, color: color }}>
          {value}
        </Typography>

        {subtitle && (
          <Typography variant="caption" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </Box>
    </Paper>
  );
}

interface StatsCardsProps {
  totalDocuments: number;
  questionsAsked: number;
  avgResponseTime: string;
  accuracy: number;
}

export default function StatsCards({
  totalDocuments,
  questionsAsked,
  avgResponseTime,
  accuracy,
}: StatsCardsProps) {
  const theme = useTheme();

  const stats = [
    {
      title: 'Total Documents',
      value: totalDocuments,
      change: 12,
      icon: <DocumentIcon />,
      color: theme.palette.primary.main,
      subtitle: 'Processed this month',
    },
    {
      title: 'Questions Asked',
      value: questionsAsked,
      change: 8,
      icon: <QuestionIcon />,
      color: theme.palette.secondary.main,
      subtitle: 'Across all documents',
    },
    {
      title: 'Avg Response Time',
      value: avgResponseTime,
      change: -5,
      icon: <SpeedIcon />,
      color: theme.palette.success.main,
      subtitle: 'Faster than last week',
    },
    {
      title: 'AI Accuracy',
      value: `${accuracy}%`,
      icon: <TrendingUpIcon />,
      color: theme.palette.info.main,
      subtitle: 'Based on user feedback',
    },
  ];

  return (
    <Grid container spacing={3}>
      {stats.map((stat, index) => (
        <Grid item xs={12} sm={6} md={3} key={index}>
          <StatCard {...stat} />
        </Grid>
      ))}
    </Grid>
  );
}
