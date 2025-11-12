import { useState, useRef, DragEvent } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  LinearProgress,
  Chip,
  IconButton,
  Alert,
  Fade,
  Zoom,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  InsertDriveFile as FileIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Close as CloseIcon,
} from '@mui/icons-material';

interface FileUploadProps {
  onUpload: (file: File) => Promise<void>;
  accept?: string;
  maxSize?: number; // in MB
  multiple?: boolean;
}

interface UploadingFile {
  file: File;
  progress: number;
  status: 'uploading' | 'success' | 'error';
  error?: string;
}

export default function FileUpload({
  onUpload,
  accept = '.pdf,.xlsx,.xls,.docx',
  maxSize = 50,
  multiple = false,
}: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadingFiles, setUploadingFiles] = useState<UploadingFile[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const validateFile = (file: File): string | null => {
    // Check file size
    if (file.size > maxSize * 1024 * 1024) {
      return `File too large. Maximum size is ${maxSize}MB`;
    }

    // Check file type
    const acceptedTypes = accept.split(',').map(t => t.trim());
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();

    if (!acceptedTypes.some(type =>
      type === fileExtension ||
      (type.includes('*') && fileExtension.match(new RegExp(type.replace('*', '.*'))))
    )) {
      return `Invalid file type. Accepted: ${accept}`;
    }

    return null;
  };

  const processFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return;

    const filesToUpload = Array.from(files);
    const newUploadingFiles: UploadingFile[] = filesToUpload.map(file => ({
      file,
      progress: 0,
      status: 'uploading' as const,
    }));

    setUploadingFiles(prev => [...prev, ...newUploadingFiles]);

    for (let i = 0; i < filesToUpload.length; i++) {
      const file = filesToUpload[i];
      const uploadIndex = uploadingFiles.length + i;

      // Validate file
      const error = validateFile(file);
      if (error) {
        setUploadingFiles(prev => prev.map((f, idx) =>
          idx === uploadIndex
            ? { ...f, status: 'error' as const, error, progress: 100 }
            : f
        ));
        continue;
      }

      try {
        // Simulate progress (replace with actual upload progress)
        const progressInterval = setInterval(() => {
          setUploadingFiles(prev => prev.map((f, idx) =>
            idx === uploadIndex && f.progress < 90
              ? { ...f, progress: f.progress + 10 }
              : f
          ));
        }, 200);

        await onUpload(file);

        clearInterval(progressInterval);

        setUploadingFiles(prev => prev.map((f, idx) =>
          idx === uploadIndex
            ? { ...f, status: 'success' as const, progress: 100 }
            : f
        ));

        // Remove success notification after 3 seconds
        setTimeout(() => {
          setUploadingFiles(prev => prev.filter((_, idx) => idx !== uploadIndex));
        }, 3000);

      } catch (err) {
        setUploadingFiles(prev => prev.map((f, idx) =>
          idx === uploadIndex
            ? {
                ...f,
                status: 'error' as const,
                error: err instanceof Error ? err.message : 'Upload failed',
                progress: 100,
              }
            : f
        ));
      }
    }
  };

  const handleDrop = async (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const { files } = e.dataTransfer;
    await processFiles(files);
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    await processFiles(e.target.files);
    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleRemove = (index: number) => {
    setUploadingFiles(prev => prev.filter((_, idx) => idx !== index));
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const getFileIcon = (fileName: string) => {
    const ext = fileName.split('.').pop()?.toLowerCase();
    const icons: Record<string, string> = {
      pdf: '📄',
      xlsx: '📊',
      xls: '📊',
      docx: '📝',
      doc: '📝',
    };
    return icons[ext || ''] || '📎';
  };

  return (
    <Box>
      {/* Drop Zone */}
      <Paper
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        sx={{
          p: 4,
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          border: '2px dashed',
          borderColor: isDragging ? 'primary.main' : 'divider',
          bgcolor: isDragging ? 'action.hover' : 'background.paper',
          transform: isDragging ? 'scale(1.02)' : 'scale(1)',
          '&:hover': {
            borderColor: 'primary.main',
            bgcolor: 'action.hover',
            transform: 'scale(1.01)',
          },
        }}
        onClick={() => fileInputRef.current?.click()}
      >
        <Zoom in={true}>
          <UploadIcon
            sx={{
              fontSize: 64,
              color: isDragging ? 'primary.main' : 'text.secondary',
              mb: 2,
              transition: 'all 0.3s ease',
            }}
          />
        </Zoom>

        <Typography variant="h6" gutterBottom>
          {isDragging ? 'Drop files here' : 'Drag & drop files here'}
        </Typography>

        <Typography variant="body2" color="text.secondary" gutterBottom>
          or
        </Typography>

        <Button
          variant="contained"
          component="span"
          startIcon={<UploadIcon />}
          sx={{ mt: 1 }}
        >
          Browse Files
        </Button>

        <Typography variant="caption" display="block" sx={{ mt: 2 }} color="text.secondary">
          Supported: {accept} • Max size: {maxSize}MB
        </Typography>

        <input
          ref={fileInputRef}
          type="file"
          accept={accept}
          multiple={multiple}
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
      </Paper>

      {/* Uploading Files */}
      {uploadingFiles.length > 0 && (
        <Box sx={{ mt: 3 }}>
          {uploadingFiles.map((uploadFile, index) => (
            <Fade key={index} in={true}>
              <Paper
                sx={{
                  p: 2,
                  mb: 1,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2,
                  transition: 'all 0.3s ease',
                }}
              >
                {/* File Icon */}
                <Typography variant="h5">
                  {getFileIcon(uploadFile.file.name)}
                </Typography>

                {/* File Info */}
                <Box sx={{ flex: 1, minWidth: 0 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                    <Typography
                      variant="body2"
                      sx={{
                        fontWeight: 500,
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {uploadFile.file.name}
                    </Typography>
                    <Chip
                      label={formatFileSize(uploadFile.file.size)}
                      size="small"
                      variant="outlined"
                    />
                  </Box>

                  {uploadFile.status === 'uploading' && (
                    <LinearProgress
                      variant="determinate"
                      value={uploadFile.progress}
                      sx={{ height: 6, borderRadius: 3 }}
                    />
                  )}

                  {uploadFile.status === 'error' && (
                    <Alert severity="error" sx={{ mt: 1, py: 0 }}>
                      {uploadFile.error}
                    </Alert>
                  )}
                </Box>

                {/* Status Icon */}
                {uploadFile.status === 'success' && (
                  <CheckIcon color="success" sx={{ fontSize: 28 }} />
                )}
                {uploadFile.status === 'error' && (
                  <ErrorIcon color="error" sx={{ fontSize: 28 }} />
                )}

                {/* Remove Button */}
                {uploadFile.status !== 'uploading' && (
                  <IconButton
                    size="small"
                    onClick={() => handleRemove(index)}
                    sx={{ opacity: 0.7, '&:hover': { opacity: 1 } }}
                  >
                    <CloseIcon fontSize="small" />
                  </IconButton>
                )}
              </Paper>
            </Fade>
          ))}
        </Box>
      )}
    </Box>
  );
}
