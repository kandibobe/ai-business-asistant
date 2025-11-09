import { useState } from 'react'
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  IconButton,
  Chip,
  LinearProgress,
} from '@mui/material'
import {
  CloudUpload,
  Description,
  PictureAsPdf,
  TableChart,
  Article,
  Link as LinkIcon,
  Delete,
  Visibility,
} from '@mui/icons-material'
import { useSelector } from 'react-redux'
import { RootState } from '@/store'

export default function DocumentsPage() {
  const { documents, isUploading, uploadProgress } = useSelector(
    (state: RootState) => state.documents
  )
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return
    // TODO: Implement upload logic
    console.log('Uploading:', selectedFile)
  }

  const getDocumentIcon = (type: string) => {
    switch (type) {
      case 'pdf':
        return <PictureAsPdf />
      case 'excel':
        return <TableChart />
      case 'word':
        return <Article />
      case 'url':
        return <LinkIcon />
      default:
        return <Description />
    }
  }

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Documents
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Upload and manage your business documents for AI analysis
        </Typography>
      </Box>

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" fontWeight={600} gutterBottom>
            Upload New Document
          </Typography>
          <Box
            sx={{
              border: '2px dashed',
              borderColor: 'divider',
              borderRadius: 2,
              p: 4,
              textAlign: 'center',
              mt: 2,
            }}
          >
            <CloudUpload sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
            <Typography variant="body1" gutterBottom>
              Drag and drop files here or click to browse
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Supported formats: PDF, Excel, Word, Audio, URLs
            </Typography>
            <Button
              variant="contained"
              component="label"
              sx={{ mt: 2 }}
              disabled={isUploading}
            >
              Select File
              <input type="file" hidden onChange={handleFileSelect} />
            </Button>
            {selectedFile && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2">
                  Selected: {selectedFile.name}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleUpload}
                  sx={{ mt: 1 }}
                  disabled={isUploading}
                >
                  Upload
                </Button>
              </Box>
            )}
            {isUploading && (
              <Box sx={{ mt: 2 }}>
                <LinearProgress variant="determinate" value={uploadProgress} />
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Uploading... {uploadProgress}%
                </Typography>
              </Box>
            )}
          </Box>
        </CardContent>
      </Card>

      <Typography variant="h6" fontWeight={600} gutterBottom>
        Your Documents ({documents.length})
      </Typography>

      <Grid container spacing={3}>
        {documents.length === 0 ? (
          <Grid item xs={12}>
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 6 }}>
                <Description sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                <Typography variant="body1" color="text.secondary">
                  No documents uploaded yet. Upload your first document to get started!
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ) : (
          documents.map((doc) => (
            <Grid item xs={12} sm={6} md={4} key={doc.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box sx={{ color: 'primary.main', mr: 2 }}>
                      {getDocumentIcon(doc.document_type)}
                    </Box>
                    <Typography variant="h6" sx={{ flex: 1 }} noWrap>
                      {doc.file_name}
                    </Typography>
                  </Box>
                  <Chip
                    label={doc.document_type.toUpperCase()}
                    size="small"
                    sx={{ mb: 2 }}
                  />
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <IconButton size="small" color="primary">
                      <Visibility />
                    </IconButton>
                    <IconButton size="small" color="error">
                      <Delete />
                    </IconButton>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
    </Box>
  )
}
