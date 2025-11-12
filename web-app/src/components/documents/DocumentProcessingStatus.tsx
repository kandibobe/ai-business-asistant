import { Box, Paper, Typography, LinearProgress, Chip, Stepper, Step, StepLabel } from '@mui/material';
import {
  UploadFile as UploadIcon,
  AutoFixHigh as ProcessIcon,
  CheckCircle as DoneIcon,
} from '@mui/icons-material';

interface DocumentProcessingStatusProps {
  fileName: string;
  currentStep: 'uploading' | 'extracting' | 'analyzing' | 'completed';
  progress: number;
}

export default function DocumentProcessingStatus({
  fileName,
  currentStep,
  progress,
}: DocumentProcessingStatusProps) {
  const steps = [
    { key: 'uploading', label: 'Uploading', icon: <UploadIcon /> },
    { key: 'extracting', label: 'Extracting Text', icon: <ProcessIcon /> },
    { key: 'analyzing', label: 'AI Analysis', icon: <ProcessIcon /> },
    { key: 'completed', label: 'Completed', icon: <DoneIcon /> },
  ];

  const currentStepIndex = steps.findIndex(step => step.key === currentStep);

  return (
    <Paper
      sx={{
        p: 3,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Animated Background */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.05) 10px, rgba(255,255,255,0.05) 20px)',
          animation: 'slide 20s linear infinite',
          '@keyframes slide': {
            '0%': { backgroundPosition: '0 0' },
            '100%': { backgroundPosition: '100px 100px' },
          },
        }}
      />

      {/* Content */}
      <Box sx={{ position: 'relative', zIndex: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Processing Document
          </Typography>
          <Chip
            label={`${progress}%`}
            sx={{
              bgcolor: 'rgba(255,255,255,0.2)',
              color: 'white',
              fontWeight: 700,
            }}
          />
        </Box>

        <Typography
          variant="body2"
          sx={{
            mb: 3,
            opacity: 0.9,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          }}
        >
          📄 {fileName}
        </Typography>

        <LinearProgress
          variant="determinate"
          value={progress}
          sx={{
            height: 8,
            borderRadius: 4,
            mb: 3,
            bgcolor: 'rgba(255,255,255,0.2)',
            '& .MuiLinearProgress-bar': {
              borderRadius: 4,
              bgcolor: 'white',
              boxShadow: '0 0 10px rgba(255,255,255,0.5)',
            },
          }}
        />

        <Stepper
          activeStep={currentStepIndex}
          alternativeLabel
          sx={{
            '& .MuiStepLabel-root': {
              color: 'rgba(255,255,255,0.7)',
            },
            '& .MuiStepLabel-label.Mui-active': {
              color: 'white',
              fontWeight: 600,
            },
            '& .MuiStepLabel-label.Mui-completed': {
              color: 'white',
            },
            '& .MuiStepIcon-root': {
              color: 'rgba(255,255,255,0.3)',
            },
            '& .MuiStepIcon-root.Mui-active': {
              color: 'white',
              boxShadow: '0 0 10px rgba(255,255,255,0.8)',
            },
            '& .MuiStepIcon-root.Mui-completed': {
              color: 'white',
            },
          }}
        >
          {steps.map((step) => (
            <Step key={step.key}>
              <StepLabel>{step.label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Box>
    </Paper>
  );
}
